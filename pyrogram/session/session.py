#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import logging
import os
import time
from datetime import datetime, timedelta
from hashlib import sha1
from io import BytesIO

import pyrogram
from pyrogram import __copyright__, __license__, __version__
from pyrogram import raw
from pyrogram.connection import Connection
from pyrogram.crypto import mtproto
from pyrogram.errors import RPCError, InternalServerError, AuthKeyDuplicated, FloodWait
from pyrogram.raw.all import layer
from pyrogram.raw.core import TLObject, MsgContainer, Int, FutureSalt, FutureSalts
from .internals import MsgId, MsgFactory

log = logging.getLogger(__name__)


class Result:
    def __init__(self):
        self.value = None
        self.event = asyncio.Event()


class Session:
    INITIAL_SALT = 0x616e67656c696361
    START_TIMEOUT = 1
    WAIT_TIMEOUT = 15
    SLEEP_THRESHOLD = 10
    MAX_RETRIES = 5
    ACKS_THRESHOLD = 8
    PING_INTERVAL = 5

    notice_displayed = False

    BAD_MSG_DESCRIPTION = {
        16: "[16] msg_id too low, the client time has to be synchronized",
        17: "[17] msg_id too high, the client time has to be synchronized",
        18: "[18] incorrect two lower order msg_id bits, the server expects client message msg_id to be divisible by 4",
        19: "[19] container msg_id is the same as msg_id of a previously received message",
        20: "[20] message too old, it cannot be verified by the server",
        32: "[32] msg_seqno too low",
        33: "[33] msg_seqno too high",
        34: "[34] an even msg_seqno expected, but odd received",
        35: "[35] odd msg_seqno expected, but even received",
        48: "[48] incorrect server salt",
        64: "[64] invalid container"
    }

    def __init__(
        self,
        client: "pyrogram.Client",
        dc_id: int,
        auth_key: bytes,
        test_mode: bool,
        is_media: bool = False,
        is_cdn: bool = False
    ):
        if not Session.notice_displayed:
            print(f"Pyrogram v{__version__}, {__copyright__}")
            print(f"Licensed under the terms of the {__license__}", end="\n\n")
            Session.notice_displayed = True

        self.client = client
        self.dc_id = dc_id
        self.auth_key = auth_key
        self.test_mode = test_mode
        self.is_media = is_media
        self.is_cdn = is_cdn

        self.connection = None

        self.auth_key_id = sha1(auth_key).digest()[-8:]

        self.session_id = os.urandom(8)
        self.msg_factory = MsgFactory()

        self.current_salt = None

        self.pending_acks = set()

        self.results = {}

        self.ping_task = None
        self.ping_task_event = asyncio.Event()

        self.next_salt_task = None
        self.next_salt_task_event = asyncio.Event()

        self.network_task = None

        self.is_connected = asyncio.Event()

        self.loop = asyncio.get_event_loop()

    async def start(self):
        while True:
            self.connection = Connection(
                self.dc_id,
                self.test_mode,
                self.client.ipv6,
                self.client.proxy
            )

            try:
                await self.connection.connect()

                self.network_task = self.loop.create_task(self.network_worker())

                self.current_salt = FutureSalt(0, 0, Session.INITIAL_SALT)
                self.current_salt = FutureSalt(
                    0, 0,
                    (await self._send(
                        raw.functions.Ping(ping_id=0),
                        timeout=self.START_TIMEOUT
                    )).new_server_salt
                )
                self.current_salt = (await self._send(
                    raw.functions.GetFutureSalts(num=1),
                    timeout=self.START_TIMEOUT)).salts[0]

                self.next_salt_task = self.loop.create_task(self.next_salt_worker())

                if not self.is_cdn:
                    await self._send(
                        raw.functions.InvokeWithLayer(
                            layer=layer,
                            query=raw.functions.InitConnection(
                                api_id=self.client.api_id,
                                app_version=self.client.app_version,
                                device_model=self.client.device_model,
                                system_version=self.client.system_version,
                                system_lang_code=self.client.lang_code,
                                lang_code=self.client.lang_code,
                                lang_pack="",
                                query=raw.functions.help.GetConfig(),
                            )
                        ),
                        timeout=self.START_TIMEOUT
                    )

                self.ping_task = self.loop.create_task(self.ping_worker())

                log.info(f"Session initialized: Layer {layer}")
                log.info(f"Device: {self.client.device_model} - {self.client.app_version}")
                log.info(f"System: {self.client.system_version} ({self.client.lang_code.upper()})")

            except AuthKeyDuplicated as e:
                await self.stop()
                raise e
            except (OSError, TimeoutError, RPCError):
                await self.stop()
            except Exception as e:
                await self.stop()
                raise e
            else:
                break

        self.is_connected.set()

        log.info("Session started")

    async def stop(self):
        self.is_connected.clear()

        self.ping_task_event.set()
        self.next_salt_task_event.set()

        if self.ping_task is not None:
            await self.ping_task

        if self.next_salt_task is not None:
            await self.next_salt_task

        self.ping_task_event.clear()
        self.next_salt_task_event.clear()

        self.connection.close()

        if self.network_task:
            await self.network_task

        for i in self.results.values():
            i.event.set()

        if not self.is_media and callable(self.client.disconnect_handler):
            try:
                await self.client.disconnect_handler(self.client)
            except Exception as e:
                log.error(e, exc_info=True)

        log.info("Session stopped")

    async def restart(self):
        await self.stop()
        await self.start()

    async def handle_packet(self, packet):
        data = await self.loop.run_in_executor(
            pyrogram.crypto_executor,
            mtproto.unpack,
            BytesIO(packet),
            self.session_id,
            self.auth_key,
            self.auth_key_id
        )

        messages = (
            data.body.messages
            if isinstance(data.body, MsgContainer)
            else [data]
        )

        # Call log.debug twice because calling it once by appending "data" to the previous string (i.e. f"Kind: {data}")
        # will cause "data" to be evaluated as string every time instead of only when debug is actually enabled.
        log.debug("Received:")
        log.debug(data)

        for msg in messages:
            if msg.seq_no == 0:
                MsgId.set_server_time(msg.msg_id / (2 ** 32))

            if msg.seq_no % 2 != 0:
                if msg.msg_id in self.pending_acks:
                    continue
                else:
                    self.pending_acks.add(msg.msg_id)

            if isinstance(msg.body, (raw.types.MsgDetailedInfo, raw.types.MsgNewDetailedInfo)):
                self.pending_acks.add(msg.body.answer_msg_id)
                continue

            if isinstance(msg.body, raw.types.NewSessionCreated):
                continue

            msg_id = None

            if isinstance(msg.body, (raw.types.BadMsgNotification, raw.types.BadServerSalt)):
                msg_id = msg.body.bad_msg_id
            elif isinstance(msg.body, (FutureSalts, raw.types.RpcResult)):
                msg_id = msg.body.req_msg_id
            elif isinstance(msg.body, raw.types.Pong):
                msg_id = msg.body.msg_id
            else:
                if self.client is not None:
                    self.loop.create_task(self.client.handle_updates(msg.body))

            if msg_id in self.results:
                self.results[msg_id].value = getattr(msg.body, "result", msg.body)
                self.results[msg_id].event.set()

        if len(self.pending_acks) >= self.ACKS_THRESHOLD:
            log.debug(f"Send {len(self.pending_acks)} acks")

            try:
                await self._send(raw.types.MsgsAck(msg_ids=list(self.pending_acks)), False)
            except (OSError, TimeoutError):
                pass
            else:
                self.pending_acks.clear()

    async def ping_worker(self):
        log.info("PingTask started")

        while True:
            try:
                await asyncio.wait_for(self.ping_task_event.wait(), self.PING_INTERVAL)
            except asyncio.TimeoutError:
                pass
            else:
                break

            try:
                await self._send(
                    raw.functions.PingDelayDisconnect(
                        ping_id=0, disconnect_delay=self.WAIT_TIMEOUT + 10
                    ), False
                )
            except (OSError, TimeoutError, RPCError):
                pass

        log.info("PingTask stopped")

    async def next_salt_worker(self):
        log.info("NextSaltTask started")

        while True:
            now = datetime.fromtimestamp(time.perf_counter() - MsgId.reference_clock + MsgId.server_time)

            # Seconds to wait until middle-overlap, which is
            # 15 minutes before/after the current/next salt end/start time
            valid_until = datetime.fromtimestamp(self.current_salt.valid_until)
            dt = (valid_until - now).total_seconds() - 900

            minutes, seconds = divmod(int(dt), 60)
            log.info(f"Next salt in {minutes:.0f}m {seconds:.0f}s (at {now + timedelta(seconds=dt)})")

            try:
                await asyncio.wait_for(self.next_salt_task_event.wait(), dt)
            except asyncio.TimeoutError:
                pass
            else:
                break

            try:
                self.current_salt = (await self._send(raw.functions.GetFutureSalts(num=1))).salts[0]
            except (OSError, TimeoutError, RPCError):
                self.connection.close()
                break

        log.info("NextSaltTask stopped")

    async def network_worker(self):
        log.info("NetworkTask started")

        while True:
            packet = await self.connection.recv()

            if packet is None or len(packet) == 4:
                if packet:
                    log.warning(f'Server sent "{Int.read(BytesIO(packet))}"')

                if self.is_connected.is_set():
                    self.loop.create_task(self.restart())

                break

            self.loop.create_task(self.handle_packet(packet))

        log.info("NetworkTask stopped")

    async def _send(self, data: TLObject, wait_response: bool = True, timeout: float = WAIT_TIMEOUT):
        message = self.msg_factory(data)
        msg_id = message.msg_id

        if wait_response:
            self.results[msg_id] = Result()

        # Call log.debug twice because calling it once by appending "data" to the previous string (i.e. f"Kind: {data}")
        # will cause "data" to be evaluated as string every time instead of only when debug is actually enabled.
        log.debug(f"Sent:")
        log.debug(message)

        payload = await self.loop.run_in_executor(
            pyrogram.crypto_executor,
            mtproto.pack,
            message,
            self.current_salt.salt,
            self.session_id,
            self.auth_key,
            self.auth_key_id
        )

        try:
            await self.connection.send(payload)
        except OSError as e:
            self.results.pop(msg_id, None)
            raise e

        if wait_response:
            try:
                await asyncio.wait_for(self.results[msg_id].event.wait(), timeout)
            except asyncio.TimeoutError:
                pass
            finally:
                result = self.results.pop(msg_id).value

            if result is None:
                raise TimeoutError
            elif isinstance(result, raw.types.RpcError):
                if isinstance(data, (raw.functions.InvokeWithoutUpdates, raw.functions.InvokeWithTakeout)):
                    data = data.query

                RPCError.raise_it(result, type(data))
            elif isinstance(result, raw.types.BadMsgNotification):
                raise Exception(self.BAD_MSG_DESCRIPTION.get(
                    result.error_code,
                    f"Error code {result.error_code}"
                ))
            else:
                return result

    async def send(
        self,
        data: TLObject,
        retries: int = MAX_RETRIES,
        timeout: float = WAIT_TIMEOUT,
        sleep_threshold: float = SLEEP_THRESHOLD
    ):
        try:
            await asyncio.wait_for(self.is_connected.wait(), self.WAIT_TIMEOUT)
        except asyncio.TimeoutError:
            pass

        if isinstance(data, (raw.functions.InvokeWithoutUpdates, raw.functions.InvokeWithTakeout)):
            query = data.query
        else:
            query = data

        query = ".".join(query.QUALNAME.split(".")[1:])

        while True:
            try:
                return await self._send(data, timeout=timeout)
            except FloodWait as e:
                amount = e.x

                if amount > sleep_threshold >= 0:
                    raise

                log.warning(f'[{self.client.session_name}] Sleeping for {amount}s (required by "{query}")')

                await asyncio.sleep(amount)
            except (OSError, TimeoutError, InternalServerError) as e:
                if retries == 0:
                    raise e from None

                (log.warning if retries < 2 else log.info)(
                    f'[{Session.MAX_RETRIES - retries + 1}] Retrying "{query}" due to {repr(e)}')

                await asyncio.sleep(0.5)

                return await self.send(data, retries - 1, timeout)

# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import asyncio
import logging
from datetime import datetime, timedelta
from hashlib import sha1
from io import BytesIO

import pyrogram
from pyrogram import __copyright__, __license__, __version__
from pyrogram.api import functions, types
from pyrogram.api.all import layer
from pyrogram.api.core import TLObject, MsgContainer, Int, Long, FutureSalt, FutureSalts
from pyrogram.connection import Connection
from pyrogram.crypto import MTProto
from pyrogram.errors import RPCError, InternalServerError, AuthKeyDuplicated
from .internals import MsgId, MsgFactory


class Result:
    def __init__(self):
        self.value = None
        self.event = asyncio.Event()


class Session:
    INITIAL_SALT = 0x616e67656c696361
    NET_WORKERS = 1
    START_TIMEOUT = 1
    WAIT_TIMEOUT = 15
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
        client: pyrogram,
        dc_id: int,
        auth_key: bytes,
        is_media: bool = False,
        is_cdn: bool = False
    ):
        if not Session.notice_displayed:
            print("Pyrogram v{}, {}".format(__version__, __copyright__))
            print("Licensed under the terms of the " + __license__, end="\n\n")
            Session.notice_displayed = True

        self.client = client
        self.dc_id = dc_id
        self.auth_key = auth_key
        self.is_media = is_media
        self.is_cdn = is_cdn

        self.connection = None

        self.auth_key_id = sha1(auth_key).digest()[-8:]

        self.session_id = Long(MsgId())
        self.msg_factory = MsgFactory()

        self.current_salt = None

        self.pending_acks = set()

        self.recv_queue = asyncio.Queue()
        self.results = {}

        self.ping_task = None
        self.ping_task_event = asyncio.Event()

        self.next_salt_task = None
        self.next_salt_task_event = asyncio.Event()

        self.net_worker_task = None
        self.recv_task = None

        self.is_connected = asyncio.Event()

    async def start(self):
        while True:
            self.connection = Connection(
                self.dc_id,
                self.client.storage.test_mode,
                self.client.ipv6,
                self.client.proxy
            )

            try:
                await self.connection.connect()

                self.net_worker_task = asyncio.ensure_future(self.net_worker())
                self.recv_task = asyncio.ensure_future(self.recv())

                self.current_salt = FutureSalt(0, 0, Session.INITIAL_SALT)
                self.current_salt = FutureSalt(
                    0, 0,
                    (await self._send(
                        functions.Ping(ping_id=0),
                        timeout=self.START_TIMEOUT
                    )).new_server_salt
                )
                self.current_salt = \
                    (await self._send(functions.GetFutureSalts(num=1), timeout=self.START_TIMEOUT)).salts[0]

                self.next_salt_task = asyncio.ensure_future(self.next_salt())

                if not self.is_cdn:
                    await self._send(
                        functions.InvokeWithLayer(
                            layer=layer,
                            query=functions.InitConnection(
                                api_id=self.client.api_id,
                                app_version=self.client.app_version,
                                device_model=self.client.device_model,
                                system_version=self.client.system_version,
                                system_lang_code=self.client.lang_code,
                                lang_code=self.client.lang_code,
                                lang_pack="",
                                query=functions.help.GetConfig(),
                            )
                        ),
                        timeout=self.START_TIMEOUT
                    )

                self.ping_task = asyncio.ensure_future(self.ping())

                logging.info("Session initialized: Layer {}".format(layer))
                logging.info("Device: {} - {}".format(self.client.device_model, self.client.app_version))
                logging.info("System: {} ({})".format(self.client.system_version, self.client.lang_code.upper()))

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

        logging.info("Session started")

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

        if self.recv_task:
            await self.recv_task

        if self.net_worker_task:
            await self.net_worker_task

        for i in self.results.values():
            i.event.set()

        if not self.is_media and callable(self.client.disconnect_handler):
            try:
                await self.client.disconnect_handler(self.client)
            except Exception as e:
                logging.error(e, exc_info=True)

        logging.info("Session stopped")

    async def restart(self):
        await self.stop()
        await self.start()

    async def net_worker(self):
        logging.info("NetWorkerTask started")

        while True:
            packet = await self.recv_queue.get()

            if packet is None:
                break

            try:
                data = MTProto.unpack(
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

                logging.debug(data)

                for msg in messages:
                    if msg.seq_no % 2 != 0:
                        if msg.msg_id in self.pending_acks:
                            continue
                        else:
                            self.pending_acks.add(msg.msg_id)

                    if isinstance(msg.body, (types.MsgDetailedInfo, types.MsgNewDetailedInfo)):
                        self.pending_acks.add(msg.body.answer_msg_id)
                        continue

                    if isinstance(msg.body, types.NewSessionCreated):
                        continue

                    msg_id = None

                    if isinstance(msg.body, (types.BadMsgNotification, types.BadServerSalt)):
                        msg_id = msg.body.bad_msg_id
                    elif isinstance(msg.body, (FutureSalts, types.RpcResult)):
                        msg_id = msg.body.req_msg_id
                    elif isinstance(msg.body, types.Pong):
                        msg_id = msg.body.msg_id
                    else:
                        if self.client is not None:
                            self.client.updates_queue.put_nowait(msg.body)

                    if msg_id in self.results:
                        self.results[msg_id].value = getattr(msg.body, "result", msg.body)
                        self.results[msg_id].event.set()

                if len(self.pending_acks) >= self.ACKS_THRESHOLD:
                    logging.info("Send {} acks".format(len(self.pending_acks)))

                    try:
                        await self._send(types.MsgsAck(msg_ids=list(self.pending_acks)), False)
                    except (OSError, TimeoutError):
                        pass
                    else:
                        self.pending_acks.clear()
            except Exception as e:
                logging.error(e, exc_info=True)

        logging.info("NetWorkerTask stopped")

    async def ping(self):
        logging.info("PingTask started")

        while True:
            try:
                await asyncio.wait_for(self.ping_task_event.wait(), self.PING_INTERVAL)
            except asyncio.TimeoutError:
                pass
            else:
                break

            try:
                await self._send(
                    functions.PingDelayDisconnect(
                        ping_id=0, disconnect_delay=self.WAIT_TIMEOUT + 10
                    ), False
                )
            except (OSError, TimeoutError, RPCError):
                pass

        logging.info("PingTask stopped")

    async def next_salt(self):
        logging.info("NextSaltTask started")

        while True:
            now = datetime.now()

            # Seconds to wait until middle-overlap, which is
            # 15 minutes before/after the current/next salt end/start time
            valid_until = datetime.fromtimestamp(self.current_salt.valid_until)
            dt = (valid_until - now).total_seconds() - 900

            logging.info("Next salt in {:.0f}m {:.0f}s ({})".format(
                dt // 60, dt % 60,
                now + timedelta(seconds=dt)
            ))

            try:
                await asyncio.wait_for(self.next_salt_task_event.wait(), dt)
            except asyncio.TimeoutError:
                pass
            else:
                break

            try:
                self.current_salt = (await self._send(functions.GetFutureSalts(num=1))).salts[0]
            except (OSError, TimeoutError, RPCError):
                self.connection.close()
                break

        logging.info("NextSaltTask stopped")

    async def recv(self):
        logging.info("RecvTask started")

        while True:
            packet = await self.connection.recv()

            if packet is None or len(packet) == 4:
                self.recv_queue.put_nowait(None)

                if packet:
                    logging.warning("Server sent \"{}\"".format(Int.read(BytesIO(packet))))

                if self.is_connected.is_set():
                    asyncio.ensure_future(self.restart())

                break

            self.recv_queue.put_nowait(packet)

        logging.info("RecvTask stopped")

    async def _send(self, data: TLObject, wait_response: bool = True, timeout: float = WAIT_TIMEOUT):
        message = self.msg_factory(data)
        msg_id = message.msg_id

        if wait_response:
            self.results[msg_id] = Result()

        payload = MTProto.pack(
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
            elif isinstance(result, types.RpcError):
                RPCError.raise_it(result, type(data))
            elif isinstance(result, types.BadMsgNotification):
                raise Exception(self.BAD_MSG_DESCRIPTION.get(
                    result.error_code,
                    "Error code {}".format(result.error_code)
                ))
            else:
                return result

    async def send(self, data: TLObject, retries: int = MAX_RETRIES, timeout: float = WAIT_TIMEOUT):
        try:
            await asyncio.wait_for(self.is_connected.wait(), self.WAIT_TIMEOUT)
        except asyncio.TimeoutError:
            pass

        try:
            return await self._send(data, timeout=timeout)
        except (OSError, TimeoutError, InternalServerError) as e:
            if retries == 0:
                raise e from None

            (log.warning if retries < 2 else log.info)(
                "[{}] Retrying {} due to {}".format(
                    Session.MAX_RETRIES - retries + 1,
                    data.QUALNAME, e))

            await asyncio.sleep(0.5)
            return await self.send(data, retries - 1, timeout)

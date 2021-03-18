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
import functools
import inspect
import logging
import os
import re
import shutil
import tempfile
from concurrent.futures.thread import ThreadPoolExecutor
from configparser import ConfigParser
from hashlib import sha256
from importlib import import_module
from pathlib import Path
from typing import Union, List, Optional

import pyrogram
from pyrogram import raw
from pyrogram import utils
from pyrogram.crypto import aes
from pyrogram.errors import (
    SessionPasswordNeeded,
    VolumeLocNotFound, ChannelPrivate,
    AuthBytesInvalid, BadRequest
)
from pyrogram.handlers.handler import Handler
from pyrogram.methods import Methods
from pyrogram.session import Auth, Session
from pyrogram.storage import Storage, FileStorage, MemoryStorage
from pyrogram.types import User, TermsOfService
from pyrogram.utils import ainput
from .dispatcher import Dispatcher
from .file_id import FileId, FileType, ThumbnailSource
from .scaffold import Scaffold

log = logging.getLogger(__name__)


class Client(Methods, Scaffold):
    """Pyrogram Client, the main means for interacting with Telegram.

    Parameters:
        session_name (``str``):
            Pass a string of your choice to give a name to the client session, e.g.: "*my_account*". This name will be
            used to save a file on disk that stores details needed to reconnect without asking again for credentials.
            Alternatively, if you don't want a file to be saved on disk, pass the special name ``":memory:"`` to start
            an in-memory session that will be discarded as soon as you stop the Client. In order to reconnect again
            using a memory storage without having to login again, you can use
            :meth:`~pyrogram.Client.export_session_string` before stopping the client to get a session string you can
            pass here as argument.

        api_id (``int`` | ``str``, *optional*):
            The *api_id* part of your Telegram API Key, as integer. E.g.: "12345".
            This is an alternative way to pass it if you don't want to use the *config.ini* file.

        api_hash (``str``, *optional*):
            The *api_hash* part of your Telegram API Key, as string. E.g.: "0123456789abcdef0123456789abcdef".
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        app_version (``str``, *optional*):
            Application version. Defaults to "Pyrogram |version|".
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        device_model (``str``, *optional*):
            Device model. Defaults to *platform.python_implementation() + " " + platform.python_version()*.
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        system_version (``str``, *optional*):
            Operating System version. Defaults to *platform.system() + " " + platform.release()*.
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        lang_code (``str``, *optional*):
            Code of the language used on the client, in ISO 639-1 standard. Defaults to "en".
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        ipv6 (``bool``, *optional*):
            Pass True to connect to Telegram using IPv6.
            Defaults to False (IPv4).

        proxy (``dict``, *optional*):
            Your SOCKS5 Proxy settings as dict,
            e.g.: *dict(hostname="11.22.33.44", port=1080, username="user", password="pass")*.
            The *username* and *password* can be omitted if your proxy doesn't require authorization.
            This is an alternative way to setup a proxy if you don't want to use the *config.ini* file.

        test_mode (``bool``, *optional*):
            Enable or disable login to the test servers.
            Only applicable for new sessions and will be ignored in case previously created sessions are loaded.
            Defaults to False.

        bot_token (``str``, *optional*):
            Pass your Bot API token to create a bot session, e.g.: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
            Only applicable for new sessions.
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        phone_number (``str``, *optional*):
            Pass your phone number as string (with your Country Code prefix included) to avoid entering it manually.
            Only applicable for new sessions.

        phone_code (``str``, *optional*):
            Pass the phone code as string (for test numbers only) to avoid entering it manually.
            Only applicable for new sessions.

        password (``str``, *optional*):
            Pass your Two-Step Verification password as string (if you have one) to avoid entering it manually.
            Only applicable for new sessions.

        force_sms (``bool``, *optional*):
            Pass True to force Telegram sending the authorization code via SMS.
            Only applicable for new sessions.
            Defaults to False.

        workers (``int``, *optional*):
            Number of maximum concurrent workers for handling incoming updates.
            Defaults to ``min(32, os.cpu_count() + 4)``.

        workdir (``str``, *optional*):
            Define a custom working directory. The working directory is the location in your filesystem where Pyrogram
            will store your session files.
            Defaults to the parent directory of the main script.

        config_file (``str``, *optional*):
            Path of the configuration file.
            Defaults to ./config.ini

        plugins (``dict``, *optional*):
            Your Smart Plugins settings as dict, e.g.: *dict(root="plugins")*.
            This is an alternative way to setup plugins if you don't want to use the *config.ini* file.

        parse_mode (``str``, *optional*):
            The parse mode, can be any of: *"combined"*, for the default combined mode. *"markdown"* or *"md"*
            to force Markdown-only styles. *"html"* to force HTML-only styles. *None* to disable the parser
            completely.

        no_updates (``bool``, *optional*):
            Pass True to completely disable incoming updates for the current session.
            When updates are disabled your client can't receive any new message.
            Useful for batch programs that don't need to deal with updates.
            Defaults to False (updates enabled and always received).

        takeout (``bool``, *optional*):
            Pass True to let the client use a takeout session instead of a normal one, implies *no_updates=True*.
            Useful for exporting your Telegram data. Methods invoked inside a takeout session (such as get_history,
            download_media, ...) are less prone to throw FloodWait exceptions.
            Only available for users, bots will ignore this parameter.
            Defaults to False (normal session).

        sleep_threshold (``int``, *optional*):
            Set a sleep threshold for flood wait exceptions happening globally in this client instance, below which any
            request that raises a flood wait will be automatically invoked again after sleeping for the required amount
            of time. Flood wait exceptions requiring higher waiting times will be raised.
            Defaults to 10 seconds.

        hide_password (``bool``, *optional*):
            Pass True to hide the password when typing it during the login.
            Defaults to False, because ``getpass`` (the library used) is known to be problematic in some
            terminal environments.
    """

    def __init__(
        self,
        session_name: Union[str, Storage],
        api_id: Union[int, str] = None,
        api_hash: str = None,
        app_version: str = None,
        device_model: str = None,
        system_version: str = None,
        lang_code: str = None,
        ipv6: bool = False,
        proxy: dict = None,
        test_mode: bool = False,
        bot_token: str = None,
        phone_number: str = None,
        phone_code: str = None,
        password: str = None,
        force_sms: bool = False,
        workers: int = Scaffold.WORKERS,
        workdir: str = Scaffold.WORKDIR,
        config_file: str = Scaffold.CONFIG_FILE,
        plugins: dict = None,
        parse_mode: str = Scaffold.PARSE_MODES[0],
        no_updates: bool = None,
        takeout: bool = None,
        sleep_threshold: int = Session.SLEEP_THRESHOLD,
        hide_password: bool = False
    ):
        super().__init__()

        self.session_name = session_name
        self.api_id = int(api_id) if api_id else None
        self.api_hash = api_hash
        self.app_version = app_version
        self.device_model = device_model
        self.system_version = system_version
        self.lang_code = lang_code
        self.ipv6 = ipv6
        # TODO: Make code consistent, use underscore for private/protected fields
        self._proxy = proxy
        self.test_mode = test_mode
        self.bot_token = bot_token
        self.phone_number = phone_number
        self.phone_code = phone_code
        self.password = password
        self.force_sms = force_sms
        self.workers = workers
        self.workdir = Path(workdir)
        self.config_file = Path(config_file)
        self.plugins = plugins
        self.parse_mode = parse_mode
        self.no_updates = no_updates
        self.takeout = takeout
        self.sleep_threshold = sleep_threshold
        self.hide_password = hide_password

        self.executor = ThreadPoolExecutor(self.workers, thread_name_prefix="Handler")

        if isinstance(session_name, str):
            if session_name == ":memory:" or len(session_name) >= MemoryStorage.SESSION_STRING_SIZE:
                session_name = re.sub(r"[\n\s]+", "", session_name)
                self.storage = MemoryStorage(session_name)
            else:
                self.storage = FileStorage(session_name, self.workdir)
        elif isinstance(session_name, Storage):
            self.storage = session_name
        else:
            raise ValueError("Unknown storage engine")

        self.dispatcher = Dispatcher(self)
        self.loop = asyncio.get_event_loop()

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        try:
            self.stop()
        except ConnectionError:
            pass

    async def __aenter__(self):
        return await self.start()

    async def __aexit__(self, *args):
        await self.stop()

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        if value is None:
            self._proxy = None
            return

        if self._proxy is None:
            self._proxy = {}

        self._proxy["enabled"] = bool(value.get("enabled", True))
        self._proxy.update(value)

    async def authorize(self) -> User:
        if self.bot_token:
            return await self.sign_in_bot(self.bot_token)

        while True:
            try:
                if not self.phone_number:
                    while True:
                        value = await ainput("Enter phone number or bot token: ")

                        if not value:
                            continue

                        confirm = (await ainput(f'Is "{value}" correct? (y/N): ')).lower()

                        if confirm == "y":
                            break

                    if ":" in value:
                        self.bot_token = value
                        return await self.sign_in_bot(value)
                    else:
                        self.phone_number = value

                sent_code = await self.send_code(self.phone_number)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_number = None
                self.bot_token = None
            else:
                break

        if self.force_sms:
            sent_code = await self.resend_code(self.phone_number, sent_code.phone_code_hash)

        print("The confirmation code has been sent via {}".format(
            {
                "app": "Telegram app",
                "sms": "SMS",
                "call": "phone call",
                "flash_call": "phone flash call"
            }[sent_code.type]
        ))

        while True:
            if not self.phone_code:
                self.phone_code = await ainput("Enter confirmation code: ")

            try:
                signed_in = await self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_code = None
            except SessionPasswordNeeded as e:
                print(e.MESSAGE)

                while True:
                    print("Password hint: {}".format(await self.get_password_hint()))

                    if not self.password:
                        self.password = await ainput("Enter password (empty to recover): ", hide=self.hide_password)

                    try:
                        if not self.password:
                            confirm = await ainput("Confirm password recovery (y/n): ")

                            if confirm == "y":
                                email_pattern = await self.send_recovery_code()
                                print(f"The recovery code has been sent to {email_pattern}")

                                while True:
                                    recovery_code = await ainput("Enter recovery code: ")

                                    try:
                                        return await self.recover_password(recovery_code)
                                    except BadRequest as e:
                                        print(e.MESSAGE)
                                    except Exception as e:
                                        log.error(e, exc_info=True)
                                        raise
                            else:
                                self.password = None
                        else:
                            return await self.check_password(self.password)
                    except BadRequest as e:
                        print(e.MESSAGE)
                        self.password = None
            else:
                break

        if isinstance(signed_in, User):
            return signed_in

        while True:
            first_name = await ainput("Enter first name: ")
            last_name = await ainput("Enter last name (empty to skip): ")

            try:
                signed_up = await self.sign_up(
                    self.phone_number,
                    sent_code.phone_code_hash,
                    first_name,
                    last_name
                )
            except BadRequest as e:
                print(e.MESSAGE)
            else:
                break

        if isinstance(signed_in, TermsOfService):
            print("\n" + signed_in.text + "\n")
            await self.accept_terms_of_service(signed_in.id)

        return signed_up

    @property
    def parse_mode(self):
        return self._parse_mode

    @parse_mode.setter
    def parse_mode(self, parse_mode: Optional[str] = "combined"):
        if parse_mode not in self.PARSE_MODES:
            raise ValueError('parse_mode must be one of {} or None. Not "{}"'.format(
                ", ".join(f'"{m}"' for m in self.PARSE_MODES[:-1]),
                parse_mode
            ))

        self._parse_mode = parse_mode

    # TODO: redundant, remove in next major version
    def set_parse_mode(self, parse_mode: Optional[str] = "combined"):
        """Set the parse mode to be used globally by the client.

        When setting the parse mode with this method, all other methods having a *parse_mode* parameter will follow the
        global value by default. The default value *"combined"* enables both Markdown and HTML styles to be used and
        combined together.

        Parameters:
            parse_mode (``str``):
                The new parse mode, can be any of: *"combined"*, for the default combined mode. *"markdown"* or *"md"*
                to force Markdown-only styles. *"html"* to force HTML-only styles. *None* to disable the parser
                completely.

        Raises:
            ValueError: In case the provided *parse_mode* is not a valid parse mode.

        Example:
            .. code-block:: python
                :emphasize-lines: 10,14,18,22

                from pyrogram import Client

                app = Client("my_account")

                with app:
                    # Default combined mode: Markdown + HTML
                    app.send_message("haskell", "1. **markdown** and <i>html</i>")

                    # Force Markdown-only, HTML is disabled
                    app.set_parse_mode("markdown")
                    app.send_message("haskell", "2. **markdown** and <i>html</i>")

                    # Force HTML-only, Markdown is disabled
                    app.set_parse_mode("html")
                    app.send_message("haskell", "3. **markdown** and <i>html</i>")

                    # Disable the parser completely
                    app.set_parse_mode(None)
                    app.send_message("haskell", "4. **markdown** and <i>html</i>")

                    # Bring back the default combined mode
                    app.set_parse_mode()
                    app.send_message("haskell", "5. **markdown** and <i>html</i>")
        """

        self.parse_mode = parse_mode

    async def fetch_peers(self, peers: List[Union[raw.types.User, raw.types.Chat, raw.types.Channel]]) -> bool:
        is_min = False
        parsed_peers = []

        for peer in peers:
            if getattr(peer, "min", False):
                is_min = True
                continue

            username = None
            phone_number = None

            if isinstance(peer, raw.types.User):
                peer_id = peer.id
                access_hash = peer.access_hash
                username = (peer.username or "").lower() or None
                phone_number = peer.phone
                peer_type = "bot" if peer.bot else "user"
            elif isinstance(peer, (raw.types.Chat, raw.types.ChatForbidden)):
                peer_id = -peer.id
                access_hash = 0
                peer_type = "group"
            elif isinstance(peer, (raw.types.Channel, raw.types.ChannelForbidden)):
                peer_id = utils.get_channel_id(peer.id)
                access_hash = peer.access_hash
                username = (getattr(peer, "username", None) or "").lower() or None
                peer_type = "channel" if peer.broadcast else "supergroup"
            else:
                continue

            parsed_peers.append((peer_id, access_hash, peer_type, username, phone_number))

        await self.storage.update_peers(parsed_peers)

        return is_min

    async def handle_download(self, packet):
        temp_file_path = ""
        final_file_path = ""

        try:
            file_id, directory, file_name, file_size, progress, progress_args = packet

            temp_file_path = await self.get_file(
                file_id=file_id,
                file_size=file_size,
                progress=progress,
                progress_args=progress_args
            )

            if temp_file_path:
                final_file_path = os.path.abspath(re.sub("\\\\", "/", os.path.join(directory, file_name)))
                os.makedirs(directory, exist_ok=True)
                shutil.move(temp_file_path, final_file_path)
        except Exception as e:
            log.error(e, exc_info=True)

            try:
                os.remove(temp_file_path)
            except OSError:
                pass
        else:
            return final_file_path or None

    async def handle_updates(self, updates):
        if isinstance(updates, (raw.types.Updates, raw.types.UpdatesCombined)):
            is_min = (await self.fetch_peers(updates.users)) or (await self.fetch_peers(updates.chats))

            users = {u.id: u for u in updates.users}
            chats = {c.id: c for c in updates.chats}

            for update in updates.updates:
                channel_id = getattr(
                    getattr(
                        getattr(
                            update, "message", None
                        ), "peer_id", None
                    ), "channel_id", None
                ) or getattr(update, "channel_id", None)

                pts = getattr(update, "pts", None)
                pts_count = getattr(update, "pts_count", None)

                if isinstance(update, raw.types.UpdateChannelTooLong):
                    log.warning(update)

                if isinstance(update, raw.types.UpdateNewChannelMessage) and is_min:
                    message = update.message

                    if not isinstance(message, raw.types.MessageEmpty):
                        try:
                            diff = await self.send(
                                raw.functions.updates.GetChannelDifference(
                                    channel=await self.resolve_peer(utils.get_channel_id(channel_id)),
                                    filter=raw.types.ChannelMessagesFilter(
                                        ranges=[raw.types.MessageRange(
                                            min_id=update.message.id,
                                            max_id=update.message.id
                                        )]
                                    ),
                                    pts=pts - pts_count,
                                    limit=pts
                                )
                            )
                        except ChannelPrivate:
                            pass
                        else:
                            if not isinstance(diff, raw.types.updates.ChannelDifferenceEmpty):
                                users.update({u.id: u for u in diff.users})
                                chats.update({c.id: c for c in diff.chats})

                self.dispatcher.updates_queue.put_nowait((update, users, chats))
        elif isinstance(updates, (raw.types.UpdateShortMessage, raw.types.UpdateShortChatMessage)):
            diff = await self.send(
                raw.functions.updates.GetDifference(
                    pts=updates.pts - updates.pts_count,
                    date=updates.date,
                    qts=-1
                )
            )

            if diff.new_messages:
                self.dispatcher.updates_queue.put_nowait((
                    raw.types.UpdateNewMessage(
                        message=diff.new_messages[0],
                        pts=updates.pts,
                        pts_count=updates.pts_count
                    ),
                    {u.id: u for u in diff.users},
                    {c.id: c for c in diff.chats}
                ))
            else:
                if diff.other_updates:  # The other_updates list can be empty
                    self.dispatcher.updates_queue.put_nowait((diff.other_updates[0], {}, {}))
        elif isinstance(updates, raw.types.UpdateShort):
            self.dispatcher.updates_queue.put_nowait((updates.update, {}, {}))
        elif isinstance(updates, raw.types.UpdatesTooLong):
            log.info(updates)

    def load_config(self):
        parser = ConfigParser()
        parser.read(str(self.config_file))

        if self.bot_token:
            pass
        else:
            self.bot_token = parser.get("pyrogram", "bot_token", fallback=None)

        if self.api_id and self.api_hash:
            pass
        else:
            if parser.has_section("pyrogram"):
                self.api_id = parser.getint("pyrogram", "api_id")
                self.api_hash = parser.get("pyrogram", "api_hash")
            else:
                raise AttributeError("No API Key found. More info: https://docs.pyrogram.org/intro/setup")

        for option in ["app_version", "device_model", "system_version", "lang_code"]:
            if getattr(self, option):
                pass
            else:
                if parser.has_section("pyrogram"):
                    setattr(self, option, parser.get(
                        "pyrogram",
                        option,
                        fallback=getattr(Client, option.upper())
                    ))
                else:
                    setattr(self, option, getattr(Client, option.upper()))

        if self._proxy:
            self._proxy["enabled"] = bool(self._proxy.get("enabled", True))
        else:
            self._proxy = {}

            if parser.has_section("proxy"):
                self._proxy["enabled"] = parser.getboolean("proxy", "enabled", fallback=True)
                self._proxy["hostname"] = parser.get("proxy", "hostname")
                self._proxy["port"] = parser.getint("proxy", "port")
                self._proxy["username"] = parser.get("proxy", "username", fallback=None) or None
                self._proxy["password"] = parser.get("proxy", "password", fallback=None) or None

        if self.plugins:
            self.plugins = {
                "enabled": bool(self.plugins.get("enabled", True)),
                "root": self.plugins.get("root", None),
                "include": self.plugins.get("include", []),
                "exclude": self.plugins.get("exclude", [])
            }
        else:
            try:
                section = parser["plugins"]

                self.plugins = {
                    "enabled": section.getboolean("enabled", True),
                    "root": section.get("root", None),
                    "include": section.get("include", []),
                    "exclude": section.get("exclude", [])
                }

                include = self.plugins["include"]
                exclude = self.plugins["exclude"]

                if include:
                    self.plugins["include"] = include.strip().split("\n")

                if exclude:
                    self.plugins["exclude"] = exclude.strip().split("\n")

            except KeyError:
                self.plugins = None

    async def load_session(self):
        await self.storage.open()

        session_empty = any([
            await self.storage.test_mode() is None,
            await self.storage.auth_key() is None,
            await self.storage.user_id() is None,
            await self.storage.is_bot() is None
        ])

        if session_empty:
            await self.storage.dc_id(2)
            await self.storage.date(0)

            await self.storage.test_mode(self.test_mode)
            await self.storage.auth_key(
                await Auth(
                    self, await self.storage.dc_id(),
                    await self.storage.test_mode()
                ).create()
            )
            await self.storage.user_id(None)
            await self.storage.is_bot(None)

    def load_plugins(self):
        if self.plugins:
            plugins = self.plugins.copy()

            for option in ["include", "exclude"]:
                if plugins[option]:
                    plugins[option] = [
                        (i.split()[0], i.split()[1:] or None)
                        for i in self.plugins[option]
                    ]
        else:
            return

        if plugins.get("enabled", False):
            root = plugins["root"]
            include = plugins["include"]
            exclude = plugins["exclude"]

            count = 0

            if not include:
                for path in sorted(Path(root.replace(".", "/")).rglob("*.py")):
                    module_path = '.'.join(path.parent.parts + (path.stem,))
                    module = import_module(module_path)

                    for name in vars(module).keys():
                        # noinspection PyBroadException
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(group, int):
                                    self.add_handler(handler, group)

                                    log.info('[{}] [LOAD] {}("{}") in group {} from "{}"'.format(
                                        self.session_name, type(handler).__name__, name, group, module_path))

                                    count += 1
                        except Exception:
                            pass
            else:
                for path, handlers in include:
                    module_path = root + "." + path
                    warn_non_existent_functions = True

                    try:
                        module = import_module(module_path)
                    except ImportError:
                        log.warning(f'[{self.session_name}] [LOAD] Ignoring non-existent module "{module_path}"')
                        continue

                    if "__path__" in dir(module):
                        log.warning(f'[{self.session_name}] [LOAD] Ignoring namespace "{module_path}"')
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        # noinspection PyBroadException
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(group, int):
                                    self.add_handler(handler, group)

                                    log.info('[{}] [LOAD] {}("{}") in group {} from "{}"'.format(
                                        self.session_name, type(handler).__name__, name, group, module_path))

                                    count += 1
                        except Exception:
                            if warn_non_existent_functions:
                                log.warning('[{}] [LOAD] Ignoring non-existent function "{}" from "{}"'.format(
                                    self.session_name, name, module_path))

            if exclude:
                for path, handlers in exclude:
                    module_path = root + "." + path
                    warn_non_existent_functions = True

                    try:
                        module = import_module(module_path)
                    except ImportError:
                        log.warning(f'[{self.session_name}] [UNLOAD] Ignoring non-existent module "{module_path}"')
                        continue

                    if "__path__" in dir(module):
                        log.warning(f'[{self.session_name}] [UNLOAD] Ignoring namespace "{module_path}"')
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        # noinspection PyBroadException
                        try:
                            for handler, group in getattr(module, name).handlers:
                                if isinstance(handler, Handler) and isinstance(group, int):
                                    self.remove_handler(handler, group)

                                    log.info('[{}] [UNLOAD] {}("{}") from group {} in "{}"'.format(
                                        self.session_name, type(handler).__name__, name, group, module_path))

                                    count -= 1
                        except Exception:
                            if warn_non_existent_functions:
                                log.warning('[{}] [UNLOAD] Ignoring non-existent function "{}" from "{}"'.format(
                                    self.session_name, name, module_path))

            if count > 0:
                log.info('[{}] Successfully loaded {} plugin{} from "{}"'.format(
                    self.session_name, count, "s" if count > 1 else "", root))
            else:
                log.warning(f'[{self.session_name}] No plugin loaded from "{root}"')

    async def get_file(
        self,
        file_id: FileId,
        file_size: int,
        progress: callable,
        progress_args: tuple = ()
    ) -> str:
        dc_id = file_id.dc_id

        async with self.media_sessions_lock:
            session = self.media_sessions.get(dc_id, None)

            if session is None:
                if dc_id != await self.storage.dc_id():
                    session = Session(
                        self, dc_id, await Auth(self, dc_id, await self.storage.test_mode()).create(),
                        await self.storage.test_mode(), is_media=True
                    )
                    await session.start()

                    for _ in range(3):
                        exported_auth = await self.send(
                            raw.functions.auth.ExportAuthorization(
                                dc_id=dc_id
                            )
                        )

                        try:
                            await session.send(
                                raw.functions.auth.ImportAuthorization(
                                    id=exported_auth.id,
                                    bytes=exported_auth.bytes
                                )
                            )
                        except AuthBytesInvalid:
                            continue
                        else:
                            break
                    else:
                        await session.stop()
                        raise AuthBytesInvalid
                else:
                    session = Session(
                        self, dc_id, await self.storage.auth_key(),
                        await self.storage.test_mode(), is_media=True
                    )
                    await session.start()

                self.media_sessions[dc_id] = session

        file_type = file_id.file_type

        if file_type == FileType.CHAT_PHOTO:
            if file_id.chat_id > 0:
                peer = raw.types.InputPeerUser(
                    user_id=file_id.chat_id,
                    access_hash=file_id.chat_access_hash
                )
            else:
                if file_id.chat_access_hash == 0:
                    peer = raw.types.InputPeerChat(
                        chat_id=-file_id.chat_id
                    )
                else:
                    peer = raw.types.InputPeerChannel(
                        channel_id=utils.get_channel_id(file_id.chat_id),
                        access_hash=file_id.chat_access_hash
                    )

            location = raw.types.InputPeerPhotoFileLocation(
                peer=peer,
                volume_id=file_id.volume_id,
                local_id=file_id.local_id,
                big=file_id.thumbnail_source == ThumbnailSource.CHAT_PHOTO_BIG
            )
        elif file_type == FileType.PHOTO:
            location = raw.types.InputPhotoFileLocation(
                id=file_id.media_id,
                access_hash=file_id.access_hash,
                file_reference=file_id.file_reference,
                thumb_size=file_id.thumbnail_size
            )
        else:
            location = raw.types.InputDocumentFileLocation(
                id=file_id.media_id,
                access_hash=file_id.access_hash,
                file_reference=file_id.file_reference,
                thumb_size=file_id.thumbnail_size
            )

        limit = 1024 * 1024
        offset = 0
        file_name = ""

        try:
            r = await session.send(
                raw.functions.upload.GetFile(
                    location=location,
                    offset=offset,
                    limit=limit
                ),
                sleep_threshold=30
            )

            if isinstance(r, raw.types.upload.File):
                with tempfile.NamedTemporaryFile("wb", delete=False) as f:
                    file_name = f.name

                    while True:
                        chunk = r.bytes

                        if not chunk:
                            break

                        f.write(chunk)

                        offset += limit

                        if progress:
                            func = functools.partial(
                                progress,
                                min(offset, file_size)
                                if file_size != 0
                                else offset,
                                file_size,
                                *progress_args
                            )

                            if inspect.iscoroutinefunction(progress):
                                await func()
                            else:
                                await self.loop.run_in_executor(self.executor, func)

                        r = await session.send(
                            raw.functions.upload.GetFile(
                                location=location,
                                offset=offset,
                                limit=limit
                            ),
                            sleep_threshold=30
                        )

            elif isinstance(r, raw.types.upload.FileCdnRedirect):
                async with self.media_sessions_lock:
                    cdn_session = self.media_sessions.get(r.dc_id, None)

                    if cdn_session is None:
                        cdn_session = Session(
                            self, r.dc_id, await Auth(self, r.dc_id, await self.storage.test_mode()).create(),
                            await self.storage.test_mode(), is_media=True, is_cdn=True
                        )

                        await cdn_session.start()

                        self.media_sessions[r.dc_id] = cdn_session

                try:
                    with tempfile.NamedTemporaryFile("wb", delete=False) as f:
                        file_name = f.name

                        while True:
                            r2 = await cdn_session.send(
                                raw.functions.upload.GetCdnFile(
                                    file_token=r.file_token,
                                    offset=offset,
                                    limit=limit
                                )
                            )

                            if isinstance(r2, raw.types.upload.CdnFileReuploadNeeded):
                                try:
                                    await session.send(
                                        raw.functions.upload.ReuploadCdnFile(
                                            file_token=r.file_token,
                                            request_token=r2.request_token
                                        )
                                    )
                                except VolumeLocNotFound:
                                    break
                                else:
                                    continue

                            chunk = r2.bytes

                            # https://core.telegram.org/cdn#decrypting-files
                            decrypted_chunk = aes.ctr256_decrypt(
                                chunk,
                                r.encryption_key,
                                bytearray(
                                    r.encryption_iv[:-4]
                                    + (offset // 16).to_bytes(4, "big")
                                )
                            )

                            hashes = await session.send(
                                raw.functions.upload.GetCdnFileHashes(
                                    file_token=r.file_token,
                                    offset=offset
                                )
                            )

                            # https://core.telegram.org/cdn#verifying-files
                            for i, h in enumerate(hashes):
                                cdn_chunk = decrypted_chunk[h.limit * i: h.limit * (i + 1)]
                                assert h.hash == sha256(cdn_chunk).digest(), f"Invalid CDN hash part {i}"

                            f.write(decrypted_chunk)

                            offset += limit

                            if progress:
                                func = functools.partial(
                                    progress,
                                    min(offset, file_size) if file_size != 0 else offset,
                                    file_size,
                                    *progress_args
                                )

                                if inspect.iscoroutinefunction(progress):
                                    await func()
                                else:
                                    await self.loop.run_in_executor(self.executor, func)

                            if len(chunk) < limit:
                                break
                except Exception as e:
                    raise e
        except Exception as e:
            if not isinstance(e, pyrogram.StopTransmission):
                log.error(e, exc_info=True)

            try:
                os.remove(file_name)
            except OSError:
                pass

            return ""
        else:
            return file_name

    def guess_mime_type(self, filename: str) -> Optional[str]:
        return self.mimetypes.guess_type(filename)[0]

    def guess_extension(self, mime_type: str) -> Optional[str]:
        return self.mimetypes.guess_extension(mime_type)

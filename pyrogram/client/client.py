# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

import base64
import binascii
import getpass
import json
import logging
import math
import mimetypes
import os
import re
import shutil
import struct
import tempfile
import threading
import time
from configparser import ConfigParser
from datetime import datetime
from hashlib import sha256, md5
from signal import signal, SIGINT, SIGTERM, SIGABRT
from threading import Thread

from pyrogram.api import functions, types
from pyrogram.api.core import Object
from pyrogram.api.errors import (
    PhoneMigrate, NetworkMigrate, PhoneNumberInvalid,
    PhoneNumberUnoccupied, PhoneCodeInvalid, PhoneCodeHashEmpty,
    PhoneCodeExpired, PhoneCodeEmpty, SessionPasswordNeeded,
    PasswordHashInvalid, FloodWait, PeerIdInvalid, FirstnameInvalid, PhoneNumberBanned,
    VolumeLocNotFound, UserMigrate, FileIdInvalid)
from pyrogram.client.handlers import DisconnectHandler
from pyrogram.crypto import AES
from pyrogram.session import Auth, Session
from .dispatcher import Dispatcher
from .ext import utils, Syncer, BaseClient
from .methods import Methods

log = logging.getLogger(__name__)


class Client(Methods, BaseClient):
    """This class represents a Client, the main mean for interacting with Telegram.
    It exposes bot-like methods for an easy access to the API as well as a simple way to
    invoke every single Telegram API method available.

    Args:
        session_name (``str``):
            Name to uniquely identify a session of either a User or a Bot.
            For Users: pass a string of your choice, e.g.: "my_main_account".
            For Bots: pass your Bot API token, e.g.: "123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
            Note: as long as a valid User session file exists, Pyrogram won't ask you again to input your phone number.

        api_id (``int``, *optional*):
            The *api_id* part of your Telegram API Key, as integer. E.g.: 12345
            This is an alternative way to pass it if you don't want to use the *config.ini* file.

        api_hash (``str``, *optional*):
            The *api_hash* part of your Telegram API Key, as string. E.g.: "0123456789abcdef0123456789abcdef"
            This is an alternative way to pass it if you don't want to use the *config.ini* file.

        app_version (``str``, *optional*):
            Application version. Defaults to "Pyrogram \U0001f525 vX.Y.Z"
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        device_model (``str``, *optional*):
            Device model. Defaults to *platform.python_implementation() + " " + platform.python_version()*
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        system_version (``str``, *optional*):
            Operating System version. Defaults to *platform.system() + " " + platform.release()*
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        lang_code (``str``, *optional*):
            Code of the language used on the client, in ISO 639-1 standard. Defaults to "en".
            This is an alternative way to set it if you don't want to use the *config.ini* file.

        proxy (``dict``, *optional*):
            Your SOCKS5 Proxy settings as dict,
            e.g.: *dict(hostname="11.22.33.44", port=1080, username="user", password="pass")*.
            *username* and *password* can be omitted if your proxy doesn't require authorization.
            This is an alternative way to setup a proxy if you don't want to use the *config.ini* file.

        test_mode (``bool``, *optional*):
            Enable or disable log-in to testing servers. Defaults to False.
            Only applicable for new sessions and will be ignored in case previously
            created sessions are loaded.

        phone_number (``str``, *optional*):
            Pass your phone number (with your Country Code prefix included) to avoid
            entering it manually. Only applicable for new sessions.

        phone_code (``str`` | ``callable``, *optional*):
            Pass the phone code as string (for test numbers only), or pass a callback function which accepts
            a single positional argument *(phone_number)* and must return the correct phone code (e.g., "12345").
            Only applicable for new sessions.

        password (``str``, *optional*):
            Pass your Two-Step Verification password (if you have one) to avoid entering it
            manually. Only applicable for new sessions.

        force_sms (``str``, *optional*):
            Pass True to force Telegram sending the authorization code via SMS.
            Only applicable for new sessions.

        first_name (``str``, *optional*):
            Pass a First Name to avoid entering it manually. It will be used to automatically
            create a new Telegram account in case the phone number you passed is not registered yet.
            Only applicable for new sessions.

        last_name (``str``, *optional*):
            Same purpose as *first_name*; pass a Last Name to avoid entering it manually. It can
            be an empty string: "". Only applicable for new sessions.

        workers (``int``, *optional*):
            Thread pool size for handling incoming updates. Defaults to 4.

        workdir (``str``, *optional*):
            Define a custom working directory. The working directory is the location in your filesystem
            where Pyrogram will store your session files. Defaults to "." (current directory).

        config_file (``str``, *optional*):
            Path of the configuration file. Defaults to ./config.ini
    """

    def __init__(self,
                 session_name: str,
                 api_id: int or str = None,
                 api_hash: str = None,
                 app_version: str = None,
                 device_model: str = None,
                 system_version: str = None,
                 lang_code: str = None,
                 proxy: dict = None,
                 test_mode: bool = False,
                 phone_number: str = None,
                 phone_code: str or callable = None,
                 password: str = None,
                 force_sms: bool = False,
                 first_name: str = None,
                 last_name: str = None,
                 workers: int = 4,
                 workdir: str = ".",
                 config_file: str = "./config.ini"):
        super().__init__()

        self.session_name = session_name
        self.api_id = int(api_id) if api_id else None
        self.api_hash = api_hash
        self.app_version = app_version
        self.device_model = device_model
        self.system_version = system_version
        self.lang_code = lang_code
        # TODO: Make code consistent, use underscore for private/protected fields
        self._proxy = proxy
        self.test_mode = test_mode
        self.phone_number = phone_number
        self.phone_code = phone_code
        self.password = password
        self.force_sms = force_sms
        self.first_name = first_name
        self.last_name = last_name
        self.workers = workers
        self.workdir = workdir
        self.config_file = config_file

        self.dispatcher = Dispatcher(self, workers)

    @property
    def proxy(self):
        return self._proxy

    @proxy.setter
    def proxy(self, value):
        self._proxy["enabled"] = True
        self._proxy.update(value)

    def start(self):
        """Use this method to start the Client after creating it.
        Requires no parameters.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        if self.is_started:
            raise ConnectionError("Client has already been started")

        if self.BOT_TOKEN_RE.match(self.session_name):
            self.token = self.session_name
            self.session_name = self.session_name.split(":")[0]

        self.load_config()
        self.load_session()

        self.session = Session(
            self,
            self.dc_id,
            self.auth_key
        )

        self.session.start()
        self.is_started = True

        if self.user_id is None:
            if self.token is None:
                self.authorize_user()
            else:
                self.authorize_bot()

            self.save_session()

        if self.token is None:
            now = time.time()

            if abs(now - self.date) > Client.OFFLINE_SLEEP:
                self.peers_by_username = {}
                self.peers_by_phone = {}

                self.get_dialogs()
                self.get_contacts()
            else:
                self.send(functions.messages.GetPinnedDialogs())
                self.get_dialogs_chunk(0)
        else:
            self.send(functions.updates.GetState())

        for i in range(self.UPDATES_WORKERS):
            self.updates_workers_list.append(
                Thread(
                    target=self.updates_worker,
                    name="UpdatesWorker#{}".format(i + 1)
                )
            )

            self.updates_workers_list[-1].start()

        for i in range(self.DOWNLOAD_WORKERS):
            self.download_workers_list.append(
                Thread(
                    target=self.download_worker,
                    name="DownloadWorker#{}".format(i + 1)
                )
            )

            self.download_workers_list[-1].start()

        self.dispatcher.start()

        mimetypes.init()
        Syncer.add(self)

    def stop(self):
        """Use this method to manually stop the Client.
        Requires no parameters.
        """
        if not self.is_started:
            raise ConnectionError("Client is already stopped")

        Syncer.remove(self)
        self.dispatcher.stop()

        for _ in range(self.DOWNLOAD_WORKERS):
            self.download_queue.put(None)

        for i in self.download_workers_list:
            i.join()

        self.download_workers_list.clear()

        for _ in range(self.UPDATES_WORKERS):
            self.updates_queue.put(None)

        for i in self.updates_workers_list:
            i.join()

        self.updates_workers_list.clear()

        for i in self.media_sessions.values():
            i.stop()

        self.media_sessions.clear()

        self.is_started = False
        self.session.stop()

    def idle(self, stop_signals: tuple = (SIGINT, SIGTERM, SIGABRT)):
        """Blocks the program execution until one of the signals are received,
        then gently stop the Client by closing the underlying connection.

        Args:
            stop_signals (``tuple``, *optional*):
                Iterable containing signals the signal handler will listen to.
                Defaults to (SIGINT, SIGTERM, SIGABRT).
        """

        def signal_handler(*args):
            self.is_idle = False

        for s in stop_signals:
            signal(s, signal_handler)

        self.is_idle = True

        while self.is_idle:
            time.sleep(1)

        self.stop()

    def run(self):
        """Use this method to automatically start and idle a Client.
        Requires no parameters.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        self.start()
        self.idle()

    def add_handler(self, handler, group: int = 0):
        """Use this method to register an update handler.

        You can register multiple handlers, but at most one handler within a group
        will be used for a single update. To handle the same update more than once, register
        your handler using a different group id (lower group id == higher priority).

        Args:
            handler (``Handler``):
                The handler to be registered.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

        Returns:
            A tuple of (handler, group)
        """
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = handler.callback
        else:
            self.dispatcher.add_handler(handler, group)

        return handler, group

    def remove_handler(self, handler, group: int = 0):
        """Removes a previously-added update handler.

        Make sure to provide the right group that the handler was added in. You can use
        the return value of the :meth:`add_handler` method, a tuple of (handler, group), and
        pass it directly.

        Args:
            handler (``Handler``):
                The handler to be removed.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = None
        else:
            self.dispatcher.remove_handler(handler, group)

    def authorize_bot(self):
        try:
            r = self.send(
                functions.auth.ImportBotAuthorization(
                    flags=0,
                    api_id=self.api_id,
                    api_hash=self.api_hash,
                    bot_auth_token=self.token
                )
            )
        except UserMigrate as e:
            self.session.stop()

            self.dc_id = e.x
            self.auth_key = Auth(self.dc_id, self.test_mode, self._proxy).create()

            self.session = Session(
                self,
                self.dc_id,
                self.auth_key
            )

            self.session.start()
            self.authorize_bot()
        else:
            self.user_id = r.user.id

    def authorize_user(self):
        phone_number_invalid_raises = self.phone_number is not None
        phone_code_invalid_raises = self.phone_code is not None
        password_hash_invalid_raises = self.password is not None
        first_name_invalid_raises = self.first_name is not None

        while True:
            if self.phone_number is None:
                self.phone_number = input("Enter phone number: ")

                while True:
                    confirm = input("Is \"{}\" correct? (y/n): ".format(self.phone_number))

                    if confirm in ("y", "1"):
                        break
                    elif confirm in ("n", "2"):
                        self.phone_number = input("Enter phone number: ")

            self.phone_number = self.phone_number.strip("+")

            try:
                r = self.send(
                    functions.auth.SendCode(
                        self.phone_number,
                        self.api_id,
                        self.api_hash
                    )
                )
            except (PhoneMigrate, NetworkMigrate) as e:
                self.session.stop()

                self.dc_id = e.x
                self.auth_key = Auth(self.dc_id, self.test_mode, self._proxy).create()

                self.session = Session(
                    self,
                    self.dc_id,
                    self.auth_key
                )
                self.session.start()

                r = self.send(
                    functions.auth.SendCode(
                        self.phone_number,
                        self.api_id,
                        self.api_hash
                    )
                )
                break
            except (PhoneNumberInvalid, PhoneNumberBanned) as e:
                if phone_number_invalid_raises:
                    raise
                else:
                    print(e.MESSAGE)
                    self.phone_number = None
            except FloodWait as e:
                if phone_number_invalid_raises:
                    raise
                else:
                    print(e.MESSAGE.format(x=e.x))
                    time.sleep(e.x)
            except Exception as e:
                log.error(e, exc_info=True)
            else:
                break

        phone_registered = r.phone_registered
        phone_code_hash = r.phone_code_hash
        terms_of_service = r.terms_of_service

        if terms_of_service:
            print("\n" + terms_of_service.text + "\n")

        if self.force_sms:
            self.send(
                functions.auth.ResendCode(
                    phone_number=self.phone_number,
                    phone_code_hash=phone_code_hash
                )
            )

        while True:
            self.phone_code = (
                input("Enter phone code: ") if self.phone_code is None
                else self.phone_code if type(self.phone_code) is str
                else str(self.phone_code(self.phone_number))
            )

            try:
                if phone_registered:
                    r = self.send(
                        functions.auth.SignIn(
                            self.phone_number,
                            phone_code_hash,
                            self.phone_code
                        )
                    )
                else:
                    try:
                        self.send(
                            functions.auth.SignIn(
                                self.phone_number,
                                phone_code_hash,
                                self.phone_code
                            )
                        )
                    except PhoneNumberUnoccupied:
                        pass

                    self.first_name = self.first_name if self.first_name is not None else input("First name: ")
                    self.last_name = self.last_name if self.last_name is not None else input("Last name: ")

                    r = self.send(
                        functions.auth.SignUp(
                            self.phone_number,
                            phone_code_hash,
                            self.phone_code,
                            self.first_name,
                            self.last_name
                        )
                    )
            except (PhoneCodeInvalid, PhoneCodeEmpty, PhoneCodeExpired, PhoneCodeHashEmpty) as e:
                if phone_code_invalid_raises:
                    raise
                else:
                    print(e.MESSAGE)
                    self.phone_code = None
            except FirstnameInvalid as e:
                if first_name_invalid_raises:
                    raise
                else:
                    print(e.MESSAGE)
                    self.first_name = None
            except SessionPasswordNeeded as e:
                print(e.MESSAGE)
                r = self.send(functions.account.GetPassword())

                while True:
                    try:

                        if self.password is None:
                            print("Hint: {}".format(r.hint))
                            self.password = getpass.getpass("Enter password: ")

                        if type(self.password) is str:
                            self.password = r.current_salt + self.password.encode() + r.current_salt

                        password_hash = sha256(self.password).digest()

                        r = self.send(functions.auth.CheckPassword(password_hash))
                    except PasswordHashInvalid as e:
                        if password_hash_invalid_raises:
                            raise
                        else:
                            print(e.MESSAGE)
                            self.password = None
                    except FloodWait as e:
                        if password_hash_invalid_raises:
                            raise
                        else:
                            print(e.MESSAGE.format(x=e.x))
                            time.sleep(e.x)
                    except Exception as e:
                        log.error(e, exc_info=True)
                    else:
                        break
                break
            except FloodWait as e:
                if phone_code_invalid_raises or first_name_invalid_raises:
                    raise
                else:
                    print(e.MESSAGE.format(x=e.x))
                    time.sleep(e.x)
            except Exception as e:
                log.error(e, exc_info=True)
            else:
                break

        if terms_of_service:
            assert self.send(functions.help.AcceptTermsOfService(terms_of_service.id))

        self.password = None
        self.user_id = r.user.id

        print("Login successful")

    def fetch_peers(self, entities: list):
        for entity in entities:
            if isinstance(entity, types.User):
                user_id = entity.id

                access_hash = entity.access_hash

                if access_hash is None:
                    continue

                username = entity.username
                phone = entity.phone

                input_peer = types.InputPeerUser(
                    user_id=user_id,
                    access_hash=access_hash
                )

                self.peers_by_id[user_id] = input_peer

                if username is not None:
                    self.peers_by_username[username.lower()] = input_peer

                if phone is not None:
                    self.peers_by_phone[phone] = input_peer

            if isinstance(entity, types.Chat):
                chat_id = entity.id
                peer_id = -chat_id

                input_peer = types.InputPeerChat(
                    chat_id=chat_id
                )

                self.peers_by_id[peer_id] = input_peer

            if isinstance(entity, types.Channel):
                channel_id = entity.id
                peer_id = int("-100" + str(channel_id))

                access_hash = entity.access_hash

                if access_hash is None:
                    continue

                username = entity.username

                input_peer = types.InputPeerChannel(
                    channel_id=channel_id,
                    access_hash=access_hash
                )

                self.peers_by_id[peer_id] = input_peer

                if username is not None:
                    self.peers_by_username[username.lower()] = input_peer

    def download_worker(self):
        name = threading.current_thread().name
        log.debug("{} started".format(name))

        while True:
            media = self.download_queue.get()

            if media is None:
                break

            temp_file_path = ""
            final_file_path = ""

            try:
                media, file_name, done, progress, progress_args, path = media

                file_id = media.file_id
                size = media.file_size

                directory, file_name = os.path.split(file_name)
                directory = directory or "downloads"

                try:
                    decoded = utils.decode(file_id)
                    fmt = "<iiqqqqi" if len(decoded) > 24 else "<iiqq"
                    unpacked = struct.unpack(fmt, decoded)
                except (AssertionError, binascii.Error, struct.error):
                    raise FileIdInvalid from None
                else:
                    media_type = unpacked[0]
                    dc_id = unpacked[1]
                    id = unpacked[2]
                    access_hash = unpacked[3]
                    volume_id = None
                    secret = None
                    local_id = None

                    if len(decoded) > 24:
                        volume_id = unpacked[4]
                        secret = unpacked[5]
                        local_id = unpacked[6]

                    media_type_str = Client.MEDIA_TYPE_ID.get(media_type, None)

                    if media_type_str is None:
                        raise FileIdInvalid("Unknown media type: {}".format(unpacked[0]))

                file_name = file_name or getattr(media, "file_name", None)

                if not file_name:
                    if media_type == 3:
                        extension = ".ogg"
                    elif media_type in (4, 10, 13):
                        extension = mimetypes.guess_extension(media.mime_type) or ".mp4"
                    elif media_type == 5:
                        extension = mimetypes.guess_extension(media.mime_type) or ".unknown"
                    elif media_type == 8:
                        extension = ".webp"
                    elif media_type == 9:
                        extension = mimetypes.guess_extension(media.mime_type) or ".mp3"
                    elif media_type in (0, 1, 2):
                        extension = ".jpg"
                    else:
                        continue

                    file_name = "{}_{}_{}{}".format(
                        media_type_str,
                        datetime.fromtimestamp(media.date or time.time()).strftime("%Y-%m-%d_%H-%M-%S"),
                        self.rnd_id(),
                        extension
                    )

                temp_file_path = self.get_file(
                    dc_id=dc_id,
                    id=id,
                    access_hash=access_hash,
                    volume_id=volume_id,
                    local_id=local_id,
                    secret=secret,
                    size=size,
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
                # TODO: "" or None for faulty download, which is better?
                # os.path methods return "" in case something does not exist, I prefer this.
                # For now let's keep None
                path[0] = final_file_path or None
            finally:
                done.set()

        log.debug("{} stopped".format(name))

    def updates_worker(self):
        name = threading.current_thread().name
        log.debug("{} started".format(name))

        while True:
            updates = self.updates_queue.get()

            if updates is None:
                break

            try:
                if isinstance(updates, (types.Update, types.UpdatesCombined)):
                    self.fetch_peers(updates.users)
                    self.fetch_peers(updates.chats)

                    for update in updates.updates:
                        channel_id = getattr(
                            getattr(
                                getattr(
                                    update, "message", None
                                ), "to_id", None
                            ), "channel_id", None
                        ) or getattr(update, "channel_id", None)

                        pts = getattr(update, "pts", None)
                        pts_count = getattr(update, "pts_count", None)

                        if isinstance(update, types.UpdateNewChannelMessage):
                            message = update.message

                            if not isinstance(message, types.MessageEmpty):
                                diff = self.send(
                                    functions.updates.GetChannelDifference(
                                        channel=self.resolve_peer(int("-100" + str(channel_id))),
                                        filter=types.ChannelMessagesFilter(
                                            ranges=[types.MessageRange(
                                                min_id=update.message.id,
                                                max_id=update.message.id
                                            )]
                                        ),
                                        pts=pts - pts_count,
                                        limit=pts
                                    )
                                )

                                if not isinstance(diff, types.updates.ChannelDifferenceEmpty):
                                    updates.users += diff.users
                                    updates.chats += diff.chats

                        if channel_id and pts:
                            if channel_id not in self.channels_pts:
                                self.channels_pts[channel_id] = []

                            if pts in self.channels_pts[channel_id]:
                                continue

                            self.channels_pts[channel_id].append(pts)

                            if len(self.channels_pts[channel_id]) > 50:
                                self.channels_pts[channel_id] = self.channels_pts[channel_id][25:]

                        self.dispatcher.updates.put((update, updates.users, updates.chats))
                elif isinstance(updates, (types.UpdateShortMessage, types.UpdateShortChatMessage)):
                    diff = self.send(
                        functions.updates.GetDifference(
                            pts=updates.pts - updates.pts_count,
                            date=updates.date,
                            qts=-1
                        )
                    )

                    if diff.new_messages:
                        self.dispatcher.updates.put((
                            types.UpdateNewMessage(
                                message=diff.new_messages[0],
                                pts=updates.pts,
                                pts_count=updates.pts_count
                            ),
                            diff.users,
                            diff.chats
                        ))
                    else:
                        self.dispatcher.updates.put((diff.other_updates[0], [], []))
                elif isinstance(updates, types.UpdateShort):
                    self.dispatcher.updates.put((updates.update, [], []))
            except Exception as e:
                log.error(e, exc_info=True)

        log.debug("{} stopped".format(name))

    def send(self, data: Object, retries: int = Session.MAX_RETRIES, timeout: float = Session.WAIT_TIMEOUT):
        """Use this method to send Raw Function queries.

        This method makes possible to manually call every single Telegram API method in a low-level manner.
        Available functions are listed in the :obj:`functions <pyrogram.api.functions>` package and may accept compound
        data types from :obj:`types <pyrogram.api.types>` as well as bare types such as ``int``, ``str``, etc...

        Args:
            data (``Object``):
                The API Scheme function filled with proper arguments.

            retries (``int``):
                Number of retries.

            timeout (``float``):
                Timeout in seconds.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        if not self.is_started:
            raise ConnectionError("Client has not been started")

        r = self.session.send(data, retries, timeout)

        self.fetch_peers(getattr(r, "users", []))
        self.fetch_peers(getattr(r, "chats", []))

        return r

    def load_config(self):
        parser = ConfigParser()
        parser.read(self.config_file)

        if self.api_id and self.api_hash:
            pass
        else:
            if parser.has_section("pyrogram"):
                self.api_id = parser.getint("pyrogram", "api_id")
                self.api_hash = parser.get("pyrogram", "api_hash")
            else:
                raise AttributeError(
                    "No API Key found. "
                    "More info: https://docs.pyrogram.ml/start/ProjectSetup#configuration"
                )

        for option in {"app_version", "device_model", "system_version", "lang_code"}:
            if getattr(self, option):
                pass
            else:
                setattr(self, option, Client.APP_VERSION)

                if parser.has_section("pyrogram"):
                    setattr(self, option, parser.get(
                        "pyrogram",
                        option,
                        fallback=getattr(Client, option.upper())
                    ))

        if self.lang_code:
            pass
        else:
            self.lang_code = Client.LANG_CODE

            if parser.has_section("pyrogram"):
                self.lang_code = parser.get(
                    "pyrogram",
                    "lang_code",
                    fallback=Client.LANG_CODE
                )

        if self._proxy:
            self._proxy["enabled"] = True
        else:
            self._proxy = {}

            if parser.has_section("proxy"):
                self._proxy["enabled"] = parser.getboolean("proxy", "enabled")
                self._proxy["hostname"] = parser.get("proxy", "hostname")
                self._proxy["port"] = parser.getint("proxy", "port")
                self._proxy["username"] = parser.get("proxy", "username", fallback=None) or None
                self._proxy["password"] = parser.get("proxy", "password", fallback=None) or None

    def load_session(self):
        try:
            with open(os.path.join(self.workdir, "{}.session".format(self.session_name)), encoding="utf-8") as f:
                s = json.load(f)
        except FileNotFoundError:
            self.dc_id = 1
            self.date = 0
            self.auth_key = Auth(self.dc_id, self.test_mode, self._proxy).create()
        else:
            self.dc_id = s["dc_id"]
            self.test_mode = s["test_mode"]
            self.auth_key = base64.b64decode("".join(s["auth_key"]))
            self.user_id = s["user_id"]
            self.date = s.get("date", 0)

            for k, v in s.get("peers_by_id", {}).items():
                self.peers_by_id[int(k)] = utils.get_input_peer(int(k), v)

            for k, v in s.get("peers_by_username", {}).items():
                peer = self.peers_by_id.get(v, None)

                if peer:
                    self.peers_by_username[k] = peer

            for k, v in s.get("peers_by_phone", {}).items():
                peer = self.peers_by_id.get(v, None)

                if peer:
                    self.peers_by_phone[k] = peer

    def save_session(self):
        auth_key = base64.b64encode(self.auth_key).decode()
        auth_key = [auth_key[i: i + 43] for i in range(0, len(auth_key), 43)]

        os.makedirs(self.workdir, exist_ok=True)

        with open(os.path.join(self.workdir, "{}.session".format(self.session_name)), "w", encoding="utf-8") as f:
            json.dump(
                dict(
                    dc_id=self.dc_id,
                    test_mode=self.test_mode,
                    auth_key=auth_key,
                    user_id=self.user_id,
                    date=self.date
                ),
                f,
                indent=4
            )

    def get_dialogs_chunk(self, offset_date):
        while True:
            try:
                r = self.send(
                    functions.messages.GetDialogs(
                        offset_date, 0, types.InputPeerEmpty(),
                        self.DIALOGS_AT_ONCE, True
                    )
                )
            except FloodWait as e:
                log.warning("get_dialogs flood: waiting {} seconds".format(e.x))
                time.sleep(e.x)
            else:
                log.info("Total peers: {}".format(len(self.peers_by_id)))
                return r

    def get_dialogs(self):
        self.send(functions.messages.GetPinnedDialogs())

        dialogs = self.get_dialogs_chunk(0)
        offset_date = utils.get_offset_date(dialogs)

        while len(dialogs.dialogs) == self.DIALOGS_AT_ONCE:
            dialogs = self.get_dialogs_chunk(offset_date)
            offset_date = utils.get_offset_date(dialogs)

        self.get_dialogs_chunk(0)

    def resolve_peer(self, peer_id: int or str):
        """Use this method to get the *InputPeer* of a known *peer_id*.

        It is intended to be used when working with Raw Functions (i.e: a Telegram API method you wish to use which is
        not available yet in the Client class as an easy-to-use method).

        Args:
            peer_id (``int`` | ``str`` | ``Peer``):
                The Peer ID you want to extract the InputPeer from. Can be one of these types: ``int`` (direct ID),
                ``str`` (@username), :obj:`PeerUser <pyrogram.api.types.PeerUser>`,
                :obj:`PeerChat <pyrogram.api.types.PeerChat>`, :obj:`PeerChannel <pyrogram.api.types.PeerChannel>`

        Returns:
            :obj:`InputPeerUser <pyrogram.api.types.InputPeerUser>` or
            :obj:`InputPeerChat <pyrogram.api.types.InputPeerChat>` or
            :obj:`InputPeerChannel <pyrogram.api.types.InputPeerChannel>` depending on the *peer_id*.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        if type(peer_id) is str:
            if peer_id in ("self", "me"):
                return types.InputPeerSelf()

            match = self.INVITE_LINK_RE.match(peer_id)

            try:
                decoded = base64.b64decode(match.group(1) + "=" * (-len(match.group(1)) % 4), "-_")
                return self.resolve_peer(struct.unpack(">2iq", decoded)[1])
            except (AttributeError, binascii.Error, struct.error):
                pass

            peer_id = re.sub(r"[@+\s]", "", peer_id.lower())

            try:
                int(peer_id)
            except ValueError:
                try:
                    return self.peers_by_username[peer_id]
                except KeyError:
                    self.send(functions.contacts.ResolveUsername(peer_id))
                    return self.peers_by_username[peer_id]
            else:
                try:
                    return self.peers_by_phone[peer_id]
                except KeyError:
                    raise PeerIdInvalid

        if type(peer_id) is not int:
            if isinstance(peer_id, types.PeerUser):
                peer_id = peer_id.user_id
            elif isinstance(peer_id, types.PeerChat):
                peer_id = -peer_id.chat_id
            elif isinstance(peer_id, types.PeerChannel):
                peer_id = int("-100" + str(peer_id.channel_id))

        try:  # User
            return self.peers_by_id[peer_id]
        except KeyError:
            try:  # Chat
                return self.peers_by_id[-peer_id]
            except KeyError:
                try:  # Channel
                    return self.peers_by_id[int("-100" + str(peer_id))]
                except (KeyError, ValueError):
                    raise PeerIdInvalid

    def save_file(self,
                  path: str,
                  file_id: int = None,
                  file_part: int = 0,
                  progress: callable = None,
                  progress_args: tuple = ()):
        part_size = 512 * 1024
        file_size = os.path.getsize(path)
        file_total_parts = int(math.ceil(file_size / part_size))
        is_big = True if file_size > 10 * 1024 * 1024 else False
        is_missing_part = True if file_id is not None else False
        file_id = file_id or self.rnd_id()
        md5_sum = md5() if not is_big and not is_missing_part else None

        session = Session(self, self.dc_id, self.auth_key, is_media=True)
        session.start()

        try:
            with open(path, "rb") as f:
                f.seek(part_size * file_part)

                while True:
                    chunk = f.read(part_size)

                    if not chunk:
                        if not is_big:
                            md5_sum = "".join([hex(i)[2:].zfill(2) for i in md5_sum.digest()])
                        break

                    if is_big:
                        rpc = functions.upload.SaveBigFilePart(
                            file_id=file_id,
                            file_part=file_part,
                            file_total_parts=file_total_parts,
                            bytes=chunk
                        )
                    else:
                        rpc = functions.upload.SaveFilePart(
                            file_id=file_id,
                            file_part=file_part,
                            bytes=chunk
                        )

                    assert session.send(rpc), "Couldn't upload file"

                    if is_missing_part:
                        return

                    if not is_big:
                        md5_sum.update(chunk)

                    file_part += 1

                    if progress:
                        progress(self, min(file_part * part_size, file_size), file_size, *progress_args)
        except Exception as e:
            log.error(e, exc_info=True)
        else:
            if is_big:
                return types.InputFileBig(
                    id=file_id,
                    parts=file_total_parts,
                    name=os.path.basename(path),

                )
            else:
                return types.InputFile(
                    id=file_id,
                    parts=file_total_parts,
                    name=os.path.basename(path),
                    md5_checksum=md5_sum
                )
        finally:
            session.stop()

    def get_file(self,
                 dc_id: int,
                 id: int = None,
                 access_hash: int = None,
                 volume_id: int = None,
                 local_id: int = None,
                 secret: int = None,
                 version: int = 0,
                 size: int = None,
                 progress: callable = None,
                 progress_args: tuple = None) -> str:
        with self.media_sessions_lock:
            session = self.media_sessions.get(dc_id, None)

            if session is None:
                if dc_id != self.dc_id:
                    exported_auth = self.send(
                        functions.auth.ExportAuthorization(
                            dc_id=dc_id
                        )
                    )

                    session = Session(
                        self,
                        dc_id,
                        Auth(dc_id, self.test_mode, self._proxy).create(),
                        is_media=True
                    )

                    session.start()

                    self.media_sessions[dc_id] = session

                    session.send(
                        functions.auth.ImportAuthorization(
                            id=exported_auth.id,
                            bytes=exported_auth.bytes
                        )
                    )
                else:
                    session = Session(
                        self,
                        dc_id,
                        self.auth_key,
                        is_media=True
                    )

                    session.start()

                    self.media_sessions[dc_id] = session

        if volume_id:  # Photos are accessed by volume_id, local_id, secret
            location = types.InputFileLocation(
                volume_id=volume_id,
                local_id=local_id,
                secret=secret
            )
        else:  # Any other file can be more easily accessed by id and access_hash
            location = types.InputDocumentFileLocation(
                id=id,
                access_hash=access_hash,
                version=version
            )

        limit = 1024 * 1024
        offset = 0
        file_name = ""

        try:
            r = session.send(
                functions.upload.GetFile(
                    location=location,
                    offset=offset,
                    limit=limit
                )
            )

            if isinstance(r, types.upload.File):
                with tempfile.NamedTemporaryFile("wb", delete=False) as f:
                    file_name = f.name

                    while True:
                        chunk = r.bytes

                        if not chunk:
                            break

                        f.write(chunk)
                        f.flush()
                        os.fsync(f.fileno())

                        offset += limit

                        if progress:
                            progress(self, min(offset, size), size, *progress_args)

                        r = session.send(
                            functions.upload.GetFile(
                                location=location,
                                offset=offset,
                                limit=limit
                            )
                        )

            elif isinstance(r, types.upload.FileCdnRedirect):
                with self.media_sessions_lock:
                    cdn_session = self.media_sessions.get(r.dc_id, None)

                    if cdn_session is None:
                        cdn_session = Session(
                            self,
                            r.dc_id,
                            Auth(r.dc_id, self.test_mode, self._proxy).create(),
                            is_media=True,
                            is_cdn=True
                        )

                        cdn_session.start()

                        self.media_sessions[r.dc_id] = cdn_session

                try:
                    with tempfile.NamedTemporaryFile("wb", delete=False) as f:
                        file_name = f.name

                        while True:
                            r2 = cdn_session.send(
                                functions.upload.GetCdnFile(
                                    file_token=r.file_token,
                                    offset=offset,
                                    limit=limit
                                )
                            )

                            if isinstance(r2, types.upload.CdnFileReuploadNeeded):
                                try:
                                    session.send(
                                        functions.upload.ReuploadCdnFile(
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
                            decrypted_chunk = AES.ctr256_decrypt(
                                chunk,
                                r.encryption_key,
                                bytearray(
                                    r.encryption_iv[:-4]
                                    + (offset // 16).to_bytes(4, "big")
                                )
                            )

                            hashes = session.send(
                                functions.upload.GetCdnFileHashes(
                                    r.file_token,
                                    offset
                                )
                            )

                            # https://core.telegram.org/cdn#verifying-files
                            for i, h in enumerate(hashes):
                                cdn_chunk = decrypted_chunk[h.limit * i: h.limit * (i + 1)]
                                assert h.hash == sha256(cdn_chunk).digest(), "Invalid CDN hash part {}".format(i)

                            f.write(decrypted_chunk)
                            f.flush()
                            os.fsync(f.fileno())

                            offset += limit

                            if progress:
                                progress(self, min(offset, size), size, *progress_args)

                            if len(chunk) < limit:
                                break
                except Exception as e:
                    raise e
        except Exception as e:
            log.error(e, exc_info=True)

            try:
                os.remove(file_name)
            except OSError:
                pass

            return ""
        else:
            return file_name

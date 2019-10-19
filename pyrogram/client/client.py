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

import logging
import math
import os
import re
import shutil
import tempfile
import threading
import time
from configparser import ConfigParser
from hashlib import sha256, md5
from importlib import import_module
from pathlib import Path
from signal import signal, SIGINT, SIGTERM, SIGABRT
from threading import Thread
from typing import Union, List

from pyrogram.api import functions, types
from pyrogram.api.core import TLObject
from pyrogram.client.handlers import DisconnectHandler
from pyrogram.client.handlers.handler import Handler
from pyrogram.client.methods.password.utils import compute_check
from pyrogram.crypto import AES
from pyrogram.errors import (
    PhoneMigrate, NetworkMigrate, SessionPasswordNeeded,
    FloodWait, PeerIdInvalid, VolumeLocNotFound, UserMigrate, ChannelPrivate, AuthBytesInvalid,
    BadRequest)
from pyrogram.session import Auth, Session
from .ext import utils, Syncer, BaseClient, Dispatcher
from .methods import Methods
from .storage import Storage, FileStorage, MemoryStorage
from .types import User, SentCode, TermsOfService

log = logging.getLogger(__name__)


class Client(Methods, BaseClient):
    """Pyrogram Client, the main means for interacting with Telegram.

    Parameters:
        session_name (``str``):
            Pass a string of your choice to give a name to the client session, e.g.: "*my_account*". This name will be
            used to save a file on disk that stores details needed to reconnect without asking again for credentials.
            Alternatively, if you don't want a file to be saved on disk, pass the special name "**:memory:**" to start
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
            Thread pool size for handling incoming updates.
            Defaults to 4.

        workdir (``str``, *optional*):
            Define a custom working directory. The working directory is the location in your filesystem where Pyrogram
            will store your session files.
            Defaults to the parent directory of the main script.

        config_file (``str``, *optional*):
            Path of the configuration file.
            Defaults to ./config.ini

        plugins (``dict``, *optional*):
            Your Smart Plugins settings as dict, e.g.: *dict(root="plugins")*.
            This is an alternative way setup plugins if you don't want to use the *config.ini* file.

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
        workers: int = BaseClient.WORKERS,
        workdir: str = BaseClient.WORKDIR,
        config_file: str = BaseClient.CONFIG_FILE,
        plugins: dict = None,
        no_updates: bool = None,
        takeout: bool = None
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
        self.no_updates = no_updates
        self.takeout = takeout

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

        self.dispatcher = Dispatcher(self, workers)

    def __enter__(self):
        return self.start()

    def __exit__(self, *args):
        try:
            self.stop()
        except ConnectionError:
            pass

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

    def connect(self) -> bool:
        """
        Connect the client to Telegram servers.

        Returns:
            ``bool``: On success, in case the passed-in session is authorized, True is returned. Otherwise, in case
            the session needs to be authorized, False is returned.

        Raises:
            ConnectionError: In case you try to connect an already connected client.
        """
        if self.is_connected:
            raise ConnectionError("Client is already connected")

        self.load_config()
        self.load_session()

        self.session = Session(self, self.storage.dc_id(), self.storage.auth_key())
        self.session.start()

        self.is_connected = True

        return bool(self.storage.user_id())

    def disconnect(self):
        """Disconnect the client from Telegram servers.

        Raises:
            ConnectionError: In case you try to disconnect an already disconnected client or in case you try to
                disconnect a client that needs to be terminated first.
        """
        if not self.is_connected:
            raise ConnectionError("Client is already disconnected")

        if self.is_initialized:
            raise ConnectionError("Can't disconnect an initialized client")

        self.session.stop()
        self.storage.close()
        self.is_connected = False

    def initialize(self):
        """Initialize the client by starting up workers.

        This method will start updates and download workers.
        It will also load plugins and start the internal dispatcher.

        Raises:
            ConnectionError: In case you try to initialize a disconnected client or in case you try to initialize an
                already initialized client.
        """
        if not self.is_connected:
            raise ConnectionError("Can't initialize a disconnected client")

        if self.is_initialized:
            raise ConnectionError("Client is already initialized")

        self.load_plugins()

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

        Syncer.add(self)

        self.is_initialized = True

    def terminate(self):
        """Terminate the client by shutting down workers.

        This method does the opposite of :meth:`~Client.initialize`.
        It will stop the dispatcher and shut down updates and download workers.

        Raises:
            ConnectionError: In case you try to terminate a client that is already terminated.
        """
        if not self.is_initialized:
            raise ConnectionError("Client is already terminated")

        if self.takeout_id:
            self.send(functions.account.FinishTakeoutSession())
            log.warning("Takeout session {} finished".format(self.takeout_id))

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

        self.is_initialized = False

    def send_code(self, phone_number: str) -> SentCode:
        """Send the confirmation code to the given phone number.

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

        Returns:
            :obj:`SentCode`: On success, an object containing information on the sent confirmation code is returned.

        Raises:
            BadRequest: In case the phone number is invalid.
        """
        phone_number = phone_number.strip(" +")

        while True:
            try:
                r = self.send(
                    functions.auth.SendCode(
                        phone_number=phone_number,
                        api_id=self.api_id,
                        api_hash=self.api_hash,
                        settings=types.CodeSettings()
                    )
                )
            except (PhoneMigrate, NetworkMigrate) as e:
                self.session.stop()

                self.storage.dc_id(e.x)
                self.storage.auth_key(Auth(self, self.storage.dc_id()).create())
                self.session = Session(self, self.storage.dc_id(), self.storage.auth_key())

                self.session.start()
            else:
                return SentCode._parse(r)

    def resend_code(self, phone_number: str, phone_code_hash: str) -> SentCode:
        """Re-send the confirmation code using a different type.

        The type of the code to be re-sent is specified in the *next_type* attribute of the :obj:`SentCode` object
        returned by :meth:`send_code`.

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            phone_code_hash (``str``):
                Confirmation code identifier.

        Returns:
            :obj:`SentCode`: On success, an object containing information on the re-sent confirmation code is returned.

        Raises:
            BadRequest: In case the arguments are invalid.
        """
        phone_number = phone_number.strip(" +")

        r = self.send(
            functions.auth.ResendCode(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash
            )
        )

        return SentCode._parse(r)

    def sign_in(self, phone_number: str, phone_code_hash: str, phone_code: str) -> Union[User, TermsOfService, bool]:
        """Authorize a user in Telegram with a valid confirmation code.

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            phone_code_hash (``str``):
                Code identifier taken from the result of :meth:`~Client.send_code`.

            phone_code (``str``):
                The valid confirmation code you received (either as Telegram message or as SMS in your phone number).

        Returns:
            :obj:`User` | :obj:`TermsOfService` | bool: On success, in case the authorization completed, the user is
            returned. In case the phone number needs to be registered first AND the terms of services accepted (with
            :meth:`~Client.accept_terms_of_service`), an object containing them is returned. In case the phone number
            needs to be registered, but the terms of services don't need to be accepted, False is returned instead.

        Raises:
            BadRequest: In case the arguments are invalid.
            SessionPasswordNeeded: In case a password is needed to sign in.
        """
        phone_number = phone_number.strip(" +")

        r = self.send(
            functions.auth.SignIn(
                phone_number=phone_number,
                phone_code_hash=phone_code_hash,
                phone_code=phone_code
            )
        )

        if isinstance(r, types.auth.AuthorizationSignUpRequired):
            if r.terms_of_service:
                return TermsOfService._parse(terms_of_service=r.terms_of_service)

            return False
        else:
            self.storage.user_id(r.user.id)
            self.storage.is_bot(False)

            return User._parse(self, r.user)

    def sign_up(self, phone_number: str, phone_code_hash: str, first_name: str, last_name: str = "") -> User:
        """Register a new user in Telegram.

        Parameters:
            phone_number (``str``):
                Phone number in international format (includes the country prefix).

            phone_code_hash (``str``):
                Code identifier taken from the result of :meth:`~Client.send_code`.

            first_name (``str``):
                New user first name.

            last_name (``str``, *optional*):
                New user last name. Defaults to "" (empty string).

        Returns:
            :obj:`User`: On success, the new registered user is returned.

        Raises:
            BadRequest: In case the arguments are invalid.
        """
        phone_number = phone_number.strip(" +")

        r = self.send(
            functions.auth.SignUp(
                phone_number=phone_number,
                first_name=first_name,
                last_name=last_name,
                phone_code_hash=phone_code_hash
            )
        )

        self.storage.user_id(r.user.id)
        self.storage.is_bot(False)

        return User._parse(self, r.user)

    def sign_in_bot(self, bot_token: str) -> User:
        """Authorize a bot using its bot token generated by BotFather.

        Parameters:
            bot_token (``str``):
                The bot token generated by BotFather

        Returns:
            :obj:`User`: On success, the bot identity is return in form of a user object.

        Raises:
            BadRequest: In case the bot token is invalid.
        """
        while True:
            try:
                r = self.send(
                    functions.auth.ImportBotAuthorization(
                        flags=0,
                        api_id=self.api_id,
                        api_hash=self.api_hash,
                        bot_auth_token=bot_token
                    )
                )
            except UserMigrate as e:
                self.session.stop()

                self.storage.dc_id(e.x)
                self.storage.auth_key(Auth(self, self.storage.dc_id()).create())
                self.session = Session(self, self.storage.dc_id(), self.storage.auth_key())

                self.session.start()
            else:
                self.storage.user_id(r.user.id)
                self.storage.is_bot(True)

                return User._parse(self, r.user)

    def get_password_hint(self) -> str:
        """Get your Two-Step Verification password hint.

        Returns:
            ``str``: On success, the password hint as string is returned.
        """
        return self.send(functions.account.GetPassword()).hint

    def check_password(self, password: str) -> User:
        """Check your Two-Step Verification password and log in.

        Parameters:
            password (``str``):
                Your Two-Step Verification password.

        Returns:
            :obj:`User`: On success, the authorized user is returned.

        Raises:
            BadRequest: In case the password is invalid.
        """
        r = self.send(
            functions.auth.CheckPassword(
                password=compute_check(
                    self.send(functions.account.GetPassword()),
                    password
                )
            )
        )

        self.storage.user_id(r.user.id)
        self.storage.is_bot(False)

        return User._parse(self, r.user)

    def send_recovery_code(self) -> str:
        """Send a code to your email to recover your password.

        Returns:
            ``str``: On success, the hidden email pattern is returned and a recovery code is sent to that email.

        Raises:
            BadRequest: In case no recovery email was set up.
        """
        return self.send(
            functions.auth.RequestPasswordRecovery()
        ).email_pattern

    def recover_password(self, recovery_code: str) -> User:
        """Recover your password with a recovery code and log in.

        Parameters:
            recovery_code (``str``):
                The recovery code sent via email.

        Returns:
            :obj:`User`: On success, the authorized user is returned and the Two-Step Verification password reset.

        Raises:
            BadRequest: In case the recovery code is invalid.
        """
        r = self.send(
            functions.auth.RecoverPassword(
                code=recovery_code
            )
        )

        self.storage.user_id(r.user.id)
        self.storage.is_bot(False)

        return User._parse(self, r.user)

    def accept_terms_of_service(self, terms_of_service_id: str) -> bool:
        """Accept the given terms of service.

        Parameters:
            terms_of_service_id (``str``):
                The terms of service identifier.
        """
        r = self.send(
            functions.help.AcceptTermsOfService(
                id=types.DataJSON(
                    data=terms_of_service_id
                )
            )
        )

        assert r

        return True

    def authorize(self) -> User:
        if self.bot_token:
            return self.sign_in_bot(self.bot_token)

        while True:
            try:
                if not self.phone_number:
                    while True:
                        value = input("Enter phone number or bot token: ")

                        if not value:
                            continue

                        confirm = input("Is \"{}\" correct? (y/N): ".format(value)).lower()

                        if confirm == "y":
                            break

                    if ":" in value:
                        self.bot_token = value
                        return self.sign_in_bot(value)
                    else:
                        self.phone_number = value

                sent_code = self.send_code(self.phone_number)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_number = None
                self.bot_token = None
            except FloodWait as e:
                print(e.MESSAGE.format(x=e.x))
                time.sleep(e.x)
            else:
                break

        if self.force_sms:
            sent_code = self.resend_code(self.phone_number, sent_code.phone_code_hash)

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
                self.phone_code = input("Enter confirmation code: ")

            try:
                signed_in = self.sign_in(self.phone_number, sent_code.phone_code_hash, self.phone_code)
            except BadRequest as e:
                print(e.MESSAGE)
                self.phone_code = None
            except SessionPasswordNeeded as e:
                print(e.MESSAGE)

                while True:
                    print("Password hint: {}".format(self.get_password_hint()))

                    if not self.password:
                        self.password = input("Enter password (empty to recover): ")

                    try:
                        if not self.password:
                            confirm = input("Confirm password recovery (y/n): ")

                            if confirm == "y":
                                email_pattern = self.send_recovery_code()
                                print("The recovery code has been sent to {}".format(email_pattern))

                                while True:
                                    recovery_code = input("Enter recovery code: ")

                                    try:
                                        return self.recover_password(recovery_code)
                                    except BadRequest as e:
                                        print(e.MESSAGE)
                                    except FloodWait as e:
                                        print(e.MESSAGE.format(x=e.x))
                                        time.sleep(e.x)
                                    except Exception as e:
                                        log.error(e, exc_info=True)
                                        raise
                            else:
                                self.password = None
                        else:
                            return self.check_password(self.password)
                    except BadRequest as e:
                        print(e.MESSAGE)
                        self.password = None
                    except FloodWait as e:
                        print(e.MESSAGE.format(x=e.x))
                        time.sleep(e.x)
            except FloodWait as e:
                print(e.MESSAGE.format(x=e.x))
                time.sleep(e.x)
            else:
                break

        if isinstance(signed_in, User):
            return signed_in

        while True:
            first_name = input("Enter first name: ")
            last_name = input("Enter last name (empty to skip): ")

            try:
                signed_up = self.sign_up(
                    self.phone_number,
                    sent_code.phone_code_hash,
                    first_name,
                    last_name
                )
            except BadRequest as e:
                print(e.MESSAGE)
            except FloodWait as e:
                print(e.MESSAGE.format(x=e.x))
                time.sleep(e.x)
            else:
                break

        if isinstance(signed_in, TermsOfService):
            print("\n" + signed_in.text + "\n")
            self.accept_terms_of_service(signed_in.id)

        return signed_up

    def log_out(self):
        """Log out from Telegram and delete the *\\*.session* file.

        When you log out, the current client is stopped and the storage session deleted.
        No more API calls can be made until you start the client and re-authorize again.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Log out.
                app.log_out()
        """
        self.send(functions.auth.LogOut())
        self.stop()
        self.storage.delete()

        return True

    def start(self):
        """Start the client.

        This method connects the client to Telegram and, in case of new sessions, automatically manages the full
        authorization process using an interactive prompt.

        Returns:
            :obj:`Client`: The started client itself.

        Raises:
            ConnectionError: In case you try to start an already started client.

        Example:
            .. code-block:: python
                :emphasize-lines: 4

                from pyrogram import Client

                app = Client("my_account")
                app.start()

                ...  # Call API methods

                app.stop()
        """
        is_authorized = self.connect()

        try:
            if not is_authorized:
                self.authorize()

            if not self.storage.is_bot() and self.takeout:
                self.takeout_id = self.send(functions.account.InitTakeoutSession()).id
                log.warning("Takeout session {} initiated".format(self.takeout_id))

            self.send(functions.updates.GetState())
        except (Exception, KeyboardInterrupt):
            self.disconnect()
            raise
        else:
            self.initialize()
            return self

    def stop(self):
        """Stop the Client.

        This method disconnects the client from Telegram and stops the underlying tasks.

        Returns:
            :obj:`Client`: The stopped client itself.

        Raises:
            ConnectionError: In case you try to stop an already stopped client.

        Example:
            .. code-block:: python
                :emphasize-lines: 8

                from pyrogram import Client

                app = Client("my_account")
                app.start()

                ...  # Call API methods

                app.stop()
        """
        self.terminate()
        self.disconnect()

        return self

    def restart(self):
        """Restart the Client.

        This method will first call :meth:`~Client.stop` and then :meth:`~Client.start` in a row in order to restart
        a client using a single method.

        Returns:
            :obj:`Client`: The restarted client itself.

        Raises:
            ConnectionError: In case you try to restart a stopped Client.

        Example:
            .. code-block:: python
                :emphasize-lines: 8

                from pyrogram import Client

                app = Client("my_account")
                app.start()

                ...  # Call API methods

                app.restart()

                ...  # Call other API methods

                app.stop()
        """
        self.stop()
        self.start()

        return self

    @staticmethod
    def idle(stop_signals: tuple = (SIGINT, SIGTERM, SIGABRT)):
        """Block the main script execution until a signal is received.

        This static method will run an infinite loop in order to block the main script execution and prevent it from
        exiting while having client(s) that are still running in the background.

        It is useful for event-driven application only, that are, applications which react upon incoming Telegram
        updates through handlers, rather than executing a set of methods sequentially.

        The way Pyrogram works, it will keep your handlers in a pool of worker threads, which are executed concurrently
        outside the main thread; calling idle() will ensure the client(s) will be kept alive by not letting the main
        script to end, until you decide to quit.

        Once a signal is received (e.g.: from CTRL+C) the inner infinite loop will break and your main script will
        continue. Don't forget to call :meth:`~Client.stop` for each running client before the script ends.

        Parameters:
            stop_signals (``tuple``, *optional*):
                Iterable containing signals the signal handler will listen to.
                Defaults to *(SIGINT, SIGTERM, SIGABRT)*.

        Example:
            .. code-block:: python
                :emphasize-lines: 13

                from pyrogram import Client

                app1 = Client("account1")
                app2 = Client("account2")
                app3 = Client("account3")

                ...  # Set handlers up

                app1.start()
                app2.start()
                app3.start()

                Client.idle()

                app1.stop()
                app2.stop()
                app3.stop()
        """

        def signal_handler(_, __):
            Client.is_idling = False

        for s in stop_signals:
            signal(s, signal_handler)

        Client.is_idling = True

        while Client.is_idling:
            time.sleep(1)

    def run(self):
        """Start the client, idle the main script and finally stop the client.

        This is a convenience method that calls :meth:`~Client.start`, :meth:`~Client.idle` and :meth:`~Client.stop` in
        sequence. It makes running a client less verbose, but is not suitable in case you want to run more than one
        client in a single main script, since idle() will block after starting the own client.

        Raises:
            ConnectionError: In case you try to run an already started client.

        Example:
            .. code-block:: python
                :emphasize-lines: 7

                from pyrogram import Client

                app = Client("my_account")

                ...  # Set handlers up

                app.run()
        """
        self.start()
        Client.idle()
        self.stop()

    def add_handler(self, handler: Handler, group: int = 0):
        """Register an update handler.

        You can register multiple handlers, but at most one handler within a group will be used for a single update.
        To handle the same update more than once, register your handler using a different group id (lower group id
        == higher priority). This mechanism is explained in greater details at
        :doc:`More on Updates <../../topics/more-on-updates>`.

        Parameters:
            handler (``Handler``):
                The handler to be registered.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

        Returns:
            ``tuple``: A tuple consisting of *(handler, group)*.

        Example:
            .. code-block:: python
                :emphasize-lines: 8

                from pyrogram import Client, MessageHandler

                def dump(client, message):
                    print(message)

                app = Client("my_account")

                app.add_handler(MessageHandler(dump))

                app.run()
        """
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = handler.callback
        else:
            self.dispatcher.add_handler(handler, group)

        return handler, group

    def remove_handler(self, handler: Handler, group: int = 0):
        """Remove a previously-registered update handler.

        Make sure to provide the right group where the handler was added in. You can use the return value of the
        :meth:`~Client.add_handler` method, a tuple of *(handler, group)*, and pass it directly.

        Parameters:
            handler (``Handler``):
                The handler to be removed.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

        Example:
            .. code-block:: python
                :emphasize-lines: 11

                from pyrogram import Client, MessageHandler

                def dump(client, message):
                    print(message)

                app = Client("my_account")

                handler = app.add_handler(MessageHandler(dump))

                # Starred expression to unpack (handler, group)
                app.remove_handler(*handler)

                app.run()
        """
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = None
        else:
            self.dispatcher.remove_handler(handler, group)

    def stop_transmission(self):
        """Stop downloading or uploading a file.

        This method must be called inside a progress callback function in order to stop the transmission at the
        desired time. The progress callback is called every time a file chunk is uploaded/downloaded.

        Example:
            .. code-block:: python
                :emphasize-lines: 9

                from pyrogram import Client

                app = Client("my_account")

                # Example to stop transmission once the upload progress reaches 50%
                # Useless in practice, but shows how to stop on command
                def progress(client, current, total):
                    if (current * 100 / total) > 50:
                        client.stop_transmission()

                with app:
                    app.send_document("me", "files.zip", progress=progress)
        """
        raise Client.StopTransmission

    def export_session_string(self):
        """Export the current authorized session as a serialized string.

        Session strings are useful for storing in-memory authorized sessions in a portable, serialized string.
        More detailed information about session strings can be found at the dedicated page of
        :doc:`Storage Engines <../../topics/storage-engines>`.

        Returns:
            ``str``: The session serialized into a printable, url-safe string.

        Example:
            .. code-block:: python
                :emphasize-lines: 6

                from pyrogram import Client

                app = Client("my_account")

                with app:
                    print(app.export_session_string())
        """
        return self.storage.export_session_string()

    def set_parse_mode(self, parse_mode: Union[str, None] = "combined"):
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

        if parse_mode not in self.PARSE_MODES:
            raise ValueError('parse_mode must be one of {} or None. Not "{}"'.format(
                ", ".join('"{}"'.format(m) for m in self.PARSE_MODES[:-1]),
                parse_mode
            ))

        self.parse_mode = parse_mode

    def fetch_peers(self, peers: List[Union[types.User, types.Chat, types.Channel]]) -> bool:
        is_min = False
        parsed_peers = []

        for peer in peers:
            if getattr(peer, "min", False):
                is_min = True
                continue

            username = None
            phone_number = None

            if isinstance(peer, types.User):
                peer_id = peer.id
                access_hash = peer.access_hash
                username = (peer.username or "").lower() or None
                phone_number = peer.phone
                peer_type = "bot" if peer.bot else "user"
            elif isinstance(peer, (types.Chat, types.ChatForbidden)):
                peer_id = -peer.id
                access_hash = 0
                peer_type = "group"
            elif isinstance(peer, (types.Channel, types.ChannelForbidden)):
                peer_id = utils.get_channel_id(peer.id)
                access_hash = peer.access_hash
                username = (getattr(peer, "username", None) or "").lower() or None
                peer_type = "channel" if peer.broadcast else "supergroup"
            else:
                continue

            parsed_peers.append((peer_id, access_hash, peer_type, username, phone_number))

        self.storage.update_peers(parsed_peers)

        return is_min

    def download_worker(self):
        name = threading.current_thread().name
        log.debug("{} started".format(name))

        while True:
            packet = self.download_queue.get()

            if packet is None:
                break

            temp_file_path = ""
            final_file_path = ""

            try:
                data, directory, file_name, done, progress, progress_args, path = packet

                temp_file_path = self.get_file(
                    media_type=data.media_type,
                    dc_id=data.dc_id,
                    document_id=data.document_id,
                    access_hash=data.access_hash,
                    thumb_size=data.thumb_size,
                    peer_id=data.peer_id,
                    peer_type=data.peer_type,
                    peer_access_hash=data.peer_access_hash,
                    volume_id=data.volume_id,
                    local_id=data.local_id,
                    file_ref=data.file_ref,
                    file_size=data.file_size,
                    is_big=data.is_big,
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
                    is_min = self.fetch_peers(updates.users) or self.fetch_peers(updates.chats)

                    users = {u.id: u for u in updates.users}
                    chats = {c.id: c for c in updates.chats}

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

                        if isinstance(update, types.UpdateChannelTooLong):
                            log.warning(update)

                        if isinstance(update, types.UpdateNewChannelMessage) and is_min:
                            message = update.message

                            if not isinstance(message, types.MessageEmpty):
                                try:
                                    diff = self.send(
                                        functions.updates.GetChannelDifference(
                                            channel=self.resolve_peer(utils.get_channel_id(channel_id)),
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
                                except ChannelPrivate:
                                    pass
                                else:
                                    if not isinstance(diff, types.updates.ChannelDifferenceEmpty):
                                        users.update({u.id: u for u in diff.users})
                                        chats.update({c.id: c for c in diff.chats})

                        self.dispatcher.updates_queue.put((update, users, chats))
                elif isinstance(updates, (types.UpdateShortMessage, types.UpdateShortChatMessage)):
                    diff = self.send(
                        functions.updates.GetDifference(
                            pts=updates.pts - updates.pts_count,
                            date=updates.date,
                            qts=-1
                        )
                    )

                    if diff.new_messages:
                        self.dispatcher.updates_queue.put((
                            types.UpdateNewMessage(
                                message=diff.new_messages[0],
                                pts=updates.pts,
                                pts_count=updates.pts_count
                            ),
                            {u.id: u for u in diff.users},
                            {c.id: c for c in diff.chats}
                        ))
                    else:
                        self.dispatcher.updates_queue.put((diff.other_updates[0], {}, {}))
                elif isinstance(updates, types.UpdateShort):
                    self.dispatcher.updates_queue.put((updates.update, {}, {}))
                elif isinstance(updates, types.UpdatesTooLong):
                    log.info(updates)
            except Exception as e:
                log.error(e, exc_info=True)

        log.debug("{} stopped".format(name))

    def send(self, data: TLObject, retries: int = Session.MAX_RETRIES, timeout: float = Session.WAIT_TIMEOUT):
        """Send raw Telegram queries.

        This method makes it possible to manually call every single Telegram API method in a low-level manner.
        Available functions are listed in the :obj:`functions <pyrogram.api.functions>` package and may accept compound
        data types from :obj:`types <pyrogram.api.types>` as well as bare types such as ``int``, ``str``, etc...

        .. note::

            This is a utility method intended to be used **only** when working with raw
            :obj:`functions <pyrogram.api.functions>` (i.e: a Telegram API method you wish to use which is not
            available yet in the Client class as an easy-to-use method).

        Parameters:
            data (``RawFunction``):
                The API Schema function filled with proper arguments.

            retries (``int``):
                Number of retries.

            timeout (``float``):
                Timeout in seconds.

        Returns:
            ``RawType``: The raw type response generated by the query.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        if self.no_updates:
            data = functions.InvokeWithoutUpdates(query=data)

        if self.takeout_id:
            data = functions.InvokeWithTakeout(takeout_id=self.takeout_id, query=data)

        r = self.session.send(data, retries, timeout)

        self.fetch_peers(getattr(r, "users", []))
        self.fetch_peers(getattr(r, "chats", []))

        return r

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

    def load_session(self):
        self.storage.open()

        session_empty = any([
            self.storage.test_mode() is None,
            self.storage.auth_key() is None,
            self.storage.user_id() is None,
            self.storage.is_bot() is None
        ])

        if session_empty:
            self.storage.dc_id(2)
            self.storage.date(0)

            self.storage.test_mode(self.test_mode)
            self.storage.auth_key(Auth(self, self.storage.dc_id()).create())
            self.storage.user_id(None)
            self.storage.is_bot(None)

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
                for path in sorted(Path(root).rglob("*.py")):
                    module_path = '.'.join(path.parent.parts + (path.stem,))
                    module = import_module(module_path)

                    for name in vars(module).keys():
                        # noinspection PyBroadException
                        try:
                            handler, group = getattr(module, name).handler

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
                        log.warning('[{}] [LOAD] Ignoring non-existent module "{}"'.format(
                            self.session_name, module_path))
                        continue

                    if "__path__" in dir(module):
                        log.warning('[{}] [LOAD] Ignoring namespace "{}"'.format(
                            self.session_name, module_path))
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        # noinspection PyBroadException
                        try:
                            handler, group = getattr(module, name).handler

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
                        log.warning('[{}] [UNLOAD] Ignoring non-existent module "{}"'.format(
                            self.session_name, module_path))
                        continue

                    if "__path__" in dir(module):
                        log.warning('[{}] [UNLOAD] Ignoring namespace "{}"'.format(
                            self.session_name, module_path))
                        continue

                    if handlers is None:
                        handlers = vars(module).keys()
                        warn_non_existent_functions = False

                    for name in handlers:
                        # noinspection PyBroadException
                        try:
                            handler, group = getattr(module, name).handler

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
                log.warning('[{}] Successfully loaded {} plugin{} from "{}"'.format(
                    self.session_name, count, "s" if count > 1 else "", root))
            else:
                log.warning('[{}] No plugin loaded from "{}"'.format(
                    self.session_name, root))

    # def get_initial_dialogs_chunk(self, offset_date: int = 0):
    #     while True:
    #         try:
    #             r = self.send(
    #                 functions.messages.GetDialogs(
    #                     offset_date=offset_date,
    #                     offset_id=0,
    #                     offset_peer=types.InputPeerEmpty(),
    #                     limit=self.DIALOGS_AT_ONCE,
    #                     hash=0,
    #                     exclude_pinned=True
    #                 )
    #             )
    #         except FloodWait as e:
    #             log.warning("get_dialogs flood: waiting {} seconds".format(e.x))
    #             time.sleep(e.x)
    #         else:
    #             log.info("Total peers: {}".format(self.storage.peers_count))
    #             return r
    #
    # def get_initial_dialogs(self):
    #     self.send(functions.messages.GetPinnedDialogs(folder_id=0))
    #
    #     dialogs = self.get_initial_dialogs_chunk()
    #     offset_date = utils.get_offset_date(dialogs)
    #
    #     while len(dialogs.dialogs) == self.DIALOGS_AT_ONCE:
    #         dialogs = self.get_initial_dialogs_chunk(offset_date)
    #         offset_date = utils.get_offset_date(dialogs)
    #
    #     self.get_initial_dialogs_chunk()

    def resolve_peer(self, peer_id: Union[int, str]):
        """Get the InputPeer of a known peer id.
        Useful whenever an InputPeer type is required.

        .. note::

            This is a utility method intended to be used **only** when working with raw
            :obj:`functions <pyrogram.api.functions>` (i.e: a Telegram API method you wish to use which is not
            available yet in the Client class as an easy-to-use method).

        Parameters:
            peer_id (``int`` | ``str``):
                The peer id you want to extract the InputPeer from.
                Can be a direct id (int), a username (str) or a phone number (str).

        Returns:
            ``InputPeer``: On success, the resolved peer id is returned in form of an InputPeer object.

        Raises:
            KeyError: In case the peer doesn't exist in the internal database.
        """
        if not self.is_connected:
            raise ConnectionError("Client has not been started yet")

        try:
            return self.storage.get_peer_by_id(peer_id)
        except KeyError:
            if type(peer_id) is str:
                if peer_id in ("self", "me"):
                    return types.InputPeerSelf()

                peer_id = re.sub(r"[@+\s]", "", peer_id.lower())

                try:
                    int(peer_id)
                except ValueError:
                    try:
                        return self.storage.get_peer_by_username(peer_id)
                    except KeyError:
                        self.send(
                            functions.contacts.ResolveUsername(
                                username=peer_id
                            )
                        )

                        return self.storage.get_peer_by_username(peer_id)
                else:
                    try:
                        return self.storage.get_peer_by_phone_number(peer_id)
                    except KeyError:
                        raise PeerIdInvalid

            peer_type = utils.get_peer_type(peer_id)

            if peer_type == "user":
                self.fetch_peers(
                    self.send(
                        functions.users.GetUsers(
                            id=[
                                types.InputUser(
                                    user_id=peer_id,
                                    access_hash=0
                                )
                            ]
                        )
                    )
                )
            elif peer_type == "chat":
                self.send(
                    functions.messages.GetChats(
                        id=[-peer_id]
                    )
                )
            else:
                self.send(
                    functions.channels.GetChannels(
                        id=[
                            types.InputChannel(
                                channel_id=utils.get_channel_id(peer_id),
                                access_hash=0
                            )
                        ]
                    )
                )

            try:
                return self.storage.get_peer_by_id(peer_id)
            except KeyError:
                raise PeerIdInvalid

    def save_file(
        self,
        path: str,
        file_id: int = None,
        file_part: int = 0,
        progress: callable = None,
        progress_args: tuple = ()
    ):
        """Upload a file onto Telegram servers, without actually sending the message to anyone.
        Useful whenever an InputFile type is required.

        .. note::

            This is a utility method intended to be used **only** when working with raw
            :obj:`functions <pyrogram.api.functions>` (i.e: a Telegram API method you wish to use which is not
            available yet in the Client class as an easy-to-use method).

        Parameters:
            path (``str``):
                The path of the file you want to upload that exists on your local machine.

            file_id (``int``, *optional*):
                In case a file part expired, pass the file_id and the file_part to retry uploading that specific chunk.

            file_part (``int``, *optional*):
                In case a file part expired, pass the file_id and the file_part to retry uploading that specific chunk.

            progress (``callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            ``InputFile``: On success, the uploaded file is returned in form of an InputFile object.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        part_size = 512 * 1024
        file_size = os.path.getsize(path)

        if file_size == 0:
            raise ValueError("File size equals to 0 B")

        if file_size > 1500 * 1024 * 1024:
            raise ValueError("Telegram doesn't support uploading files bigger than 1500 MiB")

        file_total_parts = int(math.ceil(file_size / part_size))
        is_big = True if file_size > 10 * 1024 * 1024 else False
        is_missing_part = True if file_id is not None else False
        file_id = file_id or self.rnd_id()
        md5_sum = md5() if not is_big and not is_missing_part else None

        session = Session(self, self.storage.dc_id(), self.storage.auth_key(), is_media=True)
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

                    for _ in range(3):
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

                        if session.send(rpc):
                            break
                    else:
                        raise AssertionError("Telegram didn't accept chunk #{} of {}".format(file_part, path))

                    if is_missing_part:
                        return

                    if not is_big:
                        md5_sum.update(chunk)

                    file_part += 1

                    if progress:
                        progress(min(file_part * part_size, file_size), file_size, *progress_args)
        except Client.StopTransmission:
            raise
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

    def get_file(
        self,
        media_type: int,
        dc_id: int,
        document_id: int,
        access_hash: int,
        thumb_size: str,
        peer_id: int,
        peer_type: str,
        peer_access_hash: int,
        volume_id: int,
        local_id: int,
        file_ref: str,
        file_size: int,
        is_big: bool,
        progress: callable,
        progress_args: tuple = ()
    ) -> str:
        with self.media_sessions_lock:
            session = self.media_sessions.get(dc_id, None)

            if session is None:
                if dc_id != self.storage.dc_id():
                    session = Session(self, dc_id, Auth(self, dc_id).create(), is_media=True)
                    session.start()

                    for _ in range(3):
                        exported_auth = self.send(
                            functions.auth.ExportAuthorization(
                                dc_id=dc_id
                            )
                        )

                        try:
                            session.send(
                                functions.auth.ImportAuthorization(
                                    id=exported_auth.id,
                                    bytes=exported_auth.bytes
                                )
                            )
                        except AuthBytesInvalid:
                            continue
                        else:
                            break
                    else:
                        session.stop()
                        raise AuthBytesInvalid
                else:
                    session = Session(self, dc_id, self.storage.auth_key(), is_media=True)
                    session.start()

                self.media_sessions[dc_id] = session

        file_ref = utils.decode_file_ref(file_ref)

        if media_type == 1:
            if peer_type == "user":
                peer = types.InputPeerUser(
                    user_id=peer_id,
                    access_hash=peer_access_hash
                )
            elif peer_type == "chat":
                peer = types.InputPeerChat(
                    chat_id=peer_id
                )
            else:
                peer = types.InputPeerChannel(
                    channel_id=peer_id,
                    access_hash=peer_access_hash
                )

            location = types.InputPeerPhotoFileLocation(
                peer=peer,
                volume_id=volume_id,
                local_id=local_id,
                big=is_big or None
            )
        elif media_type in (0, 2):
            location = types.InputPhotoFileLocation(
                id=document_id,
                access_hash=access_hash,
                file_reference=file_ref,
                thumb_size=thumb_size
            )
        elif media_type == 14:
            location = types.InputDocumentFileLocation(
                id=document_id,
                access_hash=access_hash,
                file_reference=file_ref,
                thumb_size=thumb_size
            )
        else:
            location = types.InputDocumentFileLocation(
                id=document_id,
                access_hash=access_hash,
                file_reference=file_ref,
                thumb_size=""
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

                        offset += limit

                        if progress:
                            progress(
                                min(offset, file_size)
                                if file_size != 0
                                else offset,
                                file_size,
                                *progress_args
                            )

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
                        cdn_session = Session(self, r.dc_id, Auth(self, r.dc_id).create(), is_media=True, is_cdn=True)

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
                                    file_token=r.file_token,
                                    offset=offset
                                )
                            )

                            # https://core.telegram.org/cdn#verifying-files
                            for i, h in enumerate(hashes):
                                cdn_chunk = decrypted_chunk[h.limit * i: h.limit * (i + 1)]
                                assert h.hash == sha256(cdn_chunk).digest(), "Invalid CDN hash part {}".format(i)

                            f.write(decrypted_chunk)

                            offset += limit

                            if progress:
                                progress(
                                    min(offset, file_size)
                                    if file_size != 0
                                    else offset,
                                    file_size,
                                    *progress_args
                                )

                            if len(chunk) < limit:
                                break
                except Exception as e:
                    raise e
        except Exception as e:
            if not isinstance(e, Client.StopTransmission):
                log.error(e, exc_info=True)

            try:
                os.remove(file_name)
            except OSError:
                pass

            return ""
        else:
            return file_name

    def guess_mime_type(self, filename: str):
        extension = os.path.splitext(filename)[1]
        return self.extensions_to_mime_types.get(extension)

    def guess_extension(self, mime_type: str):
        extensions = self.mime_types_to_extensions.get(mime_type)

        if extensions:
            return extensions.split(" ")[0]

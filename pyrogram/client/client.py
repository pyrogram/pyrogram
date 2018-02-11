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
import json
import logging
import math
import mimetypes
import os
import re
import threading
import time
from collections import namedtuple
from configparser import ConfigParser
from hashlib import sha256, md5
from queue import Queue
from signal import signal, SIGINT, SIGTERM, SIGABRT
from threading import Event, Thread

from pyrogram.api import functions, types
from pyrogram.api.core import Object
from pyrogram.api.errors import (
    PhoneMigrate, NetworkMigrate, PhoneNumberInvalid,
    PhoneNumberUnoccupied, PhoneCodeInvalid, PhoneCodeHashEmpty,
    PhoneCodeExpired, PhoneCodeEmpty, SessionPasswordNeeded,
    PasswordHashInvalid, FloodWait, PeerIdInvalid, FilePartMissing,
    ChatAdminRequired, FirstnameInvalid, PhoneNumberBanned
)
from pyrogram.api.types import (
    User, Chat, Channel,
    PeerUser, PeerChannel,
    InputPeerEmpty, InputPeerSelf,
    InputPeerUser, InputPeerChat, InputPeerChannel
)
from pyrogram.crypto import CTR
from pyrogram.session import Auth, Session
from .input_media import InputMedia
from .style import Markdown, HTML

log = logging.getLogger(__name__)

Config = namedtuple("Config", ["api_id", "api_hash"])
Proxy = namedtuple("Proxy", ["enabled", "hostname", "port", "username", "password"])


class Client:
    """This class represents a Client, the main mean for interacting with Telegram.
    It exposes bot-like methods for an easy access to the API as well as a simple way to
    invoke every single Telegram API method available.

    Args:
        session_name (:obj:`str`):
            Name to uniquely identify an authorized session. It will be used
            to save the session to a file named *<session_name>.session* and to load
            it when you restart your script. As long as a valid session file exists,
            Pyrogram won't ask you again to input your phone number.

        test_mode (:obj:`bool`, optional):
            Enable or disable log-in to testing servers. Defaults to False.
            Only applicable for new sessions and will be ignored in case previously
            created sessions are loaded.

        phone_number (:obj:`str`, optional):
            Pass your phone number (with your Country Code prefix included) to avoid
            entering it manually. Only applicable for new sessions.

        phone_code (:obj:`str` | :obj:`callable`, optional):
            Pass the phone code as string (for test numbers only), or pass a callback function
            which must return the correct phone code as string (e.g., "12345").
            Only applicable for new sessions.

        password (:obj:`str`, optional):
            Pass your Two-Step Verification password (if you have one) to avoid entering it
            manually. Only applicable for new sessions.

        first_name (:obj:`str`, optional):
            Pass a First Name to avoid entering it manually. It will be used to automatically
            create a new Telegram account in case the phone number you passed is not registered yet.

        last_name (:obj:`str`, optional):
            Same purpose as *first_name*; pass a Last Name to avoid entering it manually. It can
            be an empty string: ""

        workers (:obj:`int`, optional):
            Thread pool size for handling incoming events (updates). Defaults to 4.
    """

    INVITE_LINK_RE = re.compile(r"^(?:https?://)?t\.me/joinchat/(.+)$")
    DIALOGS_AT_ONCE = 100
    UPDATE_WORKERS = 2

    def __init__(self,
                 session_name: str,
                 test_mode: bool = False,
                 phone_number: str = None,
                 phone_code: str or callable = None,
                 password: str = None,
                 first_name: str = None,
                 last_name: str = None,
                 workers: int = 4):
        self.session_name = session_name
        self.test_mode = test_mode

        self.phone_number = phone_number
        self.password = password
        self.phone_code = phone_code
        self.first_name = first_name
        self.last_name = last_name

        self.workers = workers

        self.dc_id = None
        self.auth_key = None
        self.user_id = None

        self.rnd_id = None

        self.peers_by_id = {}
        self.peers_by_username = {}

        self.channels_pts = {}

        self.markdown = Markdown(self.peers_by_id)
        self.html = HTML(self.peers_by_id)

        self.config = None
        self.proxy = None
        self.session = None

        self.is_idle = Event()

        self.event_handler = None
        self.update_queue = Queue()
        self.event_queue = Queue()

    def start(self):
        """Use this method to start the Client after creating it.
        Requires no parameters.

        Raises:
            :class:`pyrogram.Error`
        """
        self.load_config()
        self.load_session(self.session_name)

        self.session = Session(
            self.dc_id,
            self.test_mode,
            self.proxy,
            self.auth_key,
            self.config.api_id,
            client=self
        )

        terms = self.session.start()

        if self.user_id is None:
            print("\n".join(terms.splitlines()), "\n")

            self.user_id = self.authorize()
            self.password = None
            self.save_session()

        self.rnd_id = self.session.msg_id
        self.get_dialogs()

        for i in range(self.UPDATE_WORKERS):
            Thread(target=self.update_worker, name="UpdateWorker#{}".format(i + 1)).start()

        for i in range(self.workers):
            Thread(target=self.event_worker, name="EventWorker#{}".format(i + 1)).start()

        mimetypes.init()

    def stop(self):
        """Use this method to manually stop the Client.
        Requires no parameters.
        """
        self.session.stop()

        for i in range(self.UPDATE_WORKERS):
            self.update_queue.put(None)

        for i in range(self.workers):
            self.event_queue.put(None)

    def fetch_peers(self, entities: list):
        for entity in entities:
            if isinstance(entity, User):
                user_id = entity.id

                if user_id in self.peers_by_id:
                    continue

                access_hash = entity.access_hash

                if access_hash is None:
                    continue

                username = entity.username

                input_peer = InputPeerUser(
                    user_id=user_id,
                    access_hash=access_hash
                )

                self.peers_by_id[user_id] = input_peer

                if username is not None:
                    self.peers_by_username[username] = input_peer

            if isinstance(entity, Chat):
                chat_id = entity.id

                if chat_id in self.peers_by_id:
                    continue

                input_peer = InputPeerChat(
                    chat_id=chat_id
                )

                self.peers_by_id[chat_id] = input_peer

            if isinstance(entity, Channel):
                channel_id = entity.id
                peer_id = int("-100" + str(channel_id))

                if peer_id in self.peers_by_id:
                    continue

                access_hash = entity.access_hash

                if access_hash is None:
                    continue

                username = entity.username

                input_peer = InputPeerChannel(
                    channel_id=channel_id,
                    access_hash=access_hash
                )

                self.peers_by_id[peer_id] = input_peer

                if username is not None:
                    self.peers_by_username[username] = input_peer

    def update_worker(self):
        name = threading.current_thread().name
        log.debug("{} started".format(name))

        while True:
            update = self.update_queue.get()

            if update is None:
                break

            try:
                if isinstance(update, (types.Update, types.UpdatesCombined)):
                    self.fetch_peers(update.users)
                    self.fetch_peers(update.chats)

                    for i in update.updates:
                        channel_id = getattr(
                            getattr(
                                getattr(
                                    i, "message", None
                                ), "to_id", None
                            ), "channel_id", None
                        ) or getattr(i, "channel_id", None)

                        pts = getattr(i, "pts", None)

                        if channel_id and pts:
                            if channel_id not in self.channels_pts:
                                self.channels_pts[channel_id] = []

                            if pts in self.channels_pts[channel_id]:
                                continue

                            self.channels_pts[channel_id].append(pts)

                            if len(self.channels_pts[channel_id]) > 50:
                                self.channels_pts[channel_id] = self.channels_pts[channel_id][25:]

                        self.event_queue.put((i, update.users, update.chats))
                elif isinstance(update, (types.UpdateShortMessage, types.UpdateShortChatMessage)):
                    diff = self.send(
                        functions.updates.GetDifference(
                            pts=update.pts - update.pts_count,
                            date=update.date,
                            qts=-1
                        )
                    )

                    self.fetch_peers(diff.users)
                    self.fetch_peers(diff.chats)

                    self.event_queue.put((
                        types.UpdateNewMessage(
                            message=diff.new_messages[0],
                            pts=update.pts,
                            pts_count=update.pts_count
                        ),
                        diff.users,
                        diff.chats
                    ))
                elif isinstance(update, types.UpdateShort):
                    self.event_queue.put((update.update, [], []))
            except Exception as e:
                log.error(e, exc_info=True)

        log.debug("{} stopped".format(name))

    def event_worker(self):
        name = threading.current_thread().name
        log.debug("{} started".format(name))

        while True:
            event = self.event_queue.get()

            if event is None:
                break

            try:
                if self.event_handler:
                    self.event_handler(
                        self,
                        event[0],
                        {i.id: i for i in event[1]},
                        {i.id: i for i in event[2]}
                    )
            except Exception as e:
                log.error(e, exc_info=True)

        log.debug("{} stopped".format(name))

    def signal_handler(self, *args):
        self.stop()
        self.is_idle.set()

    def idle(self, stop_signals: tuple = (SIGINT, SIGTERM, SIGABRT)):
        """Blocks the program execution until one of the signals are received,
        then gently stop the Client by closing the underlying connection.

        Args:
            stop_signals (:obj:`tuple`, optional):
                Iterable containing signals the signal handler will listen to.
                Defaults to (SIGINT, SIGTERM, SIGABRT).
        """
        for s in stop_signals:
            signal(s, self.signal_handler)

        self.is_idle.wait()

    def set_event_handler(self, callback: callable):
        """Use this method to set the event handler.

        Args:
            callback (:obj:`callable`):
                A function that takes ``client, event`` as positional arguments.
                It will be called when a new event is generated on your account.
        """
        self.event_handler = callback

    def send(self, data: Object):
        """Use this method to send :ref:`Raw Function <using-raw-functions>` queries.

        This method makes possible to manually call every single Telegram API method in a low-level manner.
        Available functions are listed in the :obj:`pyrogram.api.functions` package and may accept compound
        data types from :obj:`pyrogram.api.types` as well as bare types such as :obj:`int`, :obj:`str`, etc...

        Args:
            data (:obj:`Object`):
                The API Scheme function filled with proper arguments.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.session.send(data)

    def authorize(self):
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

            try:
                r = self.send(
                    functions.auth.SendCode(
                        self.phone_number,
                        self.config.api_id,
                        self.config.api_hash
                    )
                )
            except (PhoneMigrate, NetworkMigrate) as e:
                self.session.stop()

                self.dc_id = e.x
                self.auth_key = Auth(self.dc_id, self.test_mode, self.proxy).create()

                self.session = Session(
                    self.dc_id,
                    self.test_mode,
                    self.proxy,
                    self.auth_key,
                    self.config.api_id,
                    client=self
                )
                self.session.start()

                r = self.send(
                    functions.auth.SendCode(
                        self.phone_number,
                        self.config.api_id,
                        self.config.api_hash
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
                print(e.MESSAGE.format(x=e.x))
                time.sleep(e.x)
            except Exception as e:
                log.error(e, exc_info=True)
            else:
                break

        phone_registered = r.phone_registered
        phone_code_hash = r.phone_code_hash

        while True:
            self.phone_code = (
                input("Enter phone code: ") if self.phone_code is None
                else self.phone_code if type(self.phone_code) is str
                else self.phone_code()
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
                            self.password = input("Enter password: ")  # TODO: Use getpass

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
                        print(e.MESSAGE.format(x=e.x))
                        time.sleep(e.x)
                    except Exception as e:
                        log.error(e, exc_info=True)
                    else:
                        break
                break
            except FloodWait as e:
                print(e.MESSAGE.format(x=e.x))
                time.sleep(e.x)
            except Exception as e:
                log.error(e, exc_info=True)
            else:
                break

        return r.user.id

    def load_config(self):
        parser = ConfigParser()
        parser.read("config.ini")

        self.config = Config(
            api_id=parser.getint("pyrogram", "api_id"),
            api_hash=parser.get("pyrogram", "api_hash")
        )

        if parser.has_section("proxy"):
            self.proxy = Proxy(
                enabled=parser.getboolean("proxy", "enabled"),
                hostname=parser.get("proxy", "hostname"),
                port=parser.getint("proxy", "port"),
                username=parser.get("proxy", "username", fallback=None) or None,
                password=parser.get("proxy", "password", fallback=None) or None
            )

    def load_session(self, session_name):
        try:
            with open("{}.session".format(session_name), encoding="utf-8") as f:
                s = json.load(f)
        except FileNotFoundError:
            self.dc_id = 1
            self.auth_key = Auth(self.dc_id, self.test_mode, self.proxy).create()
        else:
            self.dc_id = s["dc_id"]
            self.test_mode = s["test_mode"]
            self.auth_key = base64.b64decode("".join(s["auth_key"]))
            self.user_id = s["user_id"]

    def save_session(self):
        auth_key = base64.b64encode(self.auth_key).decode()
        auth_key = [auth_key[i: i + 43] for i in range(0, len(auth_key), 43)]

        with open("{}.session".format(self.session_name), "w", encoding="utf-8") as f:
            json.dump(
                dict(
                    dc_id=self.dc_id,
                    test_mode=self.test_mode,
                    auth_key=auth_key,
                    user_id=self.user_id,
                ),
                f,
                indent=4
            )

    def get_dialogs(self):
        def parse_dialogs(d):
            self.fetch_peers(d.chats)
            self.fetch_peers(d.users)

            for m in reversed(d.messages):
                if isinstance(m, types.MessageEmpty):
                    continue
                else:
                    return m.date
            else:
                return 0

        pinned_dialogs = self.send(functions.messages.GetPinnedDialogs())
        parse_dialogs(pinned_dialogs)

        dialogs = self.send(
            functions.messages.GetDialogs(
                0, 0, InputPeerEmpty(),
                self.DIALOGS_AT_ONCE, True
            )
        )

        offset_date = parse_dialogs(dialogs)
        log.info("Entities count: {}".format(len(self.peers_by_id)))

        while len(dialogs.dialogs) == self.DIALOGS_AT_ONCE:
            try:
                dialogs = self.send(
                    functions.messages.GetDialogs(
                        offset_date, 0, types.InputPeerEmpty(),
                        self.DIALOGS_AT_ONCE, True
                    )
                )
            except FloodWait as e:
                log.info("Get dialogs flood wait: {}".format(e.x))
                time.sleep(e.x)
                continue

            offset_date = parse_dialogs(dialogs)
            log.info("Entities count: {}".format(len(self.peers_by_id)))

    def resolve_username(self, username: str):
        username = username.lower().strip("@")

        resolved_peer = self.send(
            functions.contacts.ResolveUsername(
                username=username
            )
        )  # type: types.contacts.ResolvedPeer

        if type(resolved_peer.peer) is PeerUser:
            input_peer = InputPeerUser(
                user_id=resolved_peer.users[0].id,
                access_hash=resolved_peer.users[0].access_hash
            )
            peer_id = input_peer.user_id
        elif type(resolved_peer.peer) is PeerChannel:
            input_peer = InputPeerChannel(
                channel_id=resolved_peer.chats[0].id,
                access_hash=resolved_peer.chats[0].access_hash
            )
            peer_id = int("-100" + str(input_peer.channel_id))
        else:
            raise PeerIdInvalid

        self.peers_by_username[username] = input_peer
        self.peers_by_id[peer_id] = input_peer

        return input_peer

    def resolve_peer(self, peer_id: int or str):
        if peer_id in ("self", "me"):
            return InputPeerSelf()
        else:
            if type(peer_id) is str:
                peer_id = peer_id.lower().strip("@")

                try:
                    return self.peers_by_username[peer_id]
                except KeyError:
                    return self.resolve_username(peer_id)
            else:
                try:
                    return self.peers_by_id[peer_id]
                except KeyError:
                    try:
                        return self.peers_by_id[int("-100" + str(peer_id))]
                    except KeyError:
                        raise PeerIdInvalid

    def get_me(self):
        """A simple method for testing the user authorization. Requires no parameters.

        Returns:
            Full information about the user in form of a :obj:`UserFull <pyrogram.api.types.UserFull>` object.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.users.GetFullUser(
                InputPeerSelf()
            )
        )

    def send_message(self,
                     chat_id: int or str,
                     text: str,
                     parse_mode: str = "",
                     disable_web_page_preview: bool = None,
                     disable_notification: bool = None,
                     reply_to_message_id: int = None):
        """Use this method to send text messages.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            text (:obj:`str`):
                Text of the message to be sent.

            parse_mode (:obj:`str`):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your message.
                Defaults to Markdown.

            disable_web_page_preview (:obj:`bool`, optional):
                Disables link previews for links in this message.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`bool`, optional):
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown

        return self.send(
            functions.messages.SendMessage(
                peer=self.resolve_peer(chat_id),
                no_webpage=disable_web_page_preview or None,
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id(),
                **style.parse(text)
            )
        )

    def forward_messages(self,
                         chat_id: int or str,
                         from_chat_id: int or str,
                         message_ids: list,
                         disable_notification: bool = None):
        """Use this method to forward messages of any kind.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            from_chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the chat where the original message was sent
                (or channel/supergroup username in the format @username). For your personal cloud
                storage (Saved Messages) you can simply use "me" or "self".

            message_ids (:obj:`list`):
                A list of Message identifiers in the chat specified in *from_chat_id*.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.messages.ForwardMessages(
                to_peer=self.resolve_peer(chat_id),
                from_peer=self.resolve_peer(from_chat_id),
                id=message_ids,
                silent=disable_notification or None,
                random_id=[self.rnd_id() for _ in message_ids]
            )
        )

    def send_photo(self,
                   chat_id: int or str,
                   photo: str,
                   caption: str = "",
                   parse_mode: str = "",
                   ttl_seconds: int = None,
                   disable_notification: bool = None,
                   reply_to_message_id: int = None):
        """Use this method to send photos.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            photo (:obj:`str`):
                Photo to send.
                Pass a file path as string to send a photo that exists on your local machine.

            caption (:obj:`bool`, optional):
                Photo caption, 0-200 characters.

            parse_mode (:obj:`str`):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            ttl_seconds (:obj:`int`, optional):
                Self-Destruct Timer.
                If you set a timer, the photo will self-destruct in :obj:`ttl_seconds`
                seconds after it was viewed.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown
        file = self.save_file(photo)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedPhoto(
                            file=file,
                            ttl_seconds=ttl_seconds
                        ),
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id(),
                        **style.parse(caption)
                    )
                )
            except FilePartMissing as e:
                self.save_file(photo, file_id=file.id, file_part=e.x)
            else:
                return r

    def send_audio(self,
                   chat_id: int or str,
                   audio: str,
                   caption: str = "",
                   parse_mode: str = "",
                   duration: int = 0,
                   performer: str = None,
                   title: str = None,
                   disable_notification: bool = None,
                   reply_to_message_id: int = None):
        """Use this method to send audio files.

        For sending voice messages, use the :obj:`send_voice` method instead.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            audio (:obj:`str`):
                Audio file to send.
                Pass a file path as string to send an audio file that exists on your local machine.

            caption (:obj:`str`, optional):
                Audio caption, 0-200 characters.

            parse_mode (:obj:`str`):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            duration (:obj:`int`, optional):
                Duration of the audio in seconds.

            performer (:obj:`str`, optional):
                Performer.

            title (:obj:`str`, optional):
                Track name.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown
        file = self.save_file(audio)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=mimetypes.types_map.get("." + audio.split(".")[-1], "audio/mpeg"),
                            file=file,
                            attributes=[
                                types.DocumentAttributeAudio(
                                    duration=duration,
                                    performer=performer,
                                    title=title
                                ),
                                types.DocumentAttributeFilename(os.path.basename(audio))
                            ]
                        ),
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id(),
                        **style.parse(caption)
                    )
                )
            except FilePartMissing as e:
                self.save_file(audio, file_id=file.id, file_part=e.x)
            else:
                return r

    def send_document(self,
                      chat_id: int or str,
                      document: str,
                      caption: str = "",
                      parse_mode: str = "",
                      disable_notification: bool = None,
                      reply_to_message_id: int = None):
        """Use this method to send general files.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            document (:obj:`str`):
                File to send.
                Pass a file path as string to send a file that exists on your local machine.

            caption (:obj:`str`, optional):
                Document caption, 0-200 characters.

            parse_mode (:obj:`str`):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown
        file = self.save_file(document)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=mimetypes.types_map.get("." + document.split(".")[-1], "text/plain"),
                            file=file,
                            attributes=[
                                types.DocumentAttributeFilename(os.path.basename(document))
                            ]
                        ),
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id(),
                        **style.parse(caption)
                    )
                )
            except FilePartMissing as e:
                self.save_file(document, file_id=file.id, file_part=e.x)
            else:
                return r

    def send_video(self,
                   chat_id: int or str,
                   video: str,
                   caption: str = "",
                   parse_mode: str = "",
                   duration: int = 0,
                   width: int = 0,
                   height: int = 0,
                   disable_notification: bool = None,
                   reply_to_message_id: int = None):
        """Use this method to send video files.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            video (:obj:`str`):
                Video to send.
                Pass a file path as string to send a video that exists on your local machine.

            caption (:obj:`str`, optional):
                Video caption, 0-200 characters.

            parse_mode (:obj:`str`):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            duration (:obj:`int`, optional):
                Duration of sent video in seconds.

            width (:obj:`int`, optional):
                Video width.

            height (:obj:`int`, optional):
                Video height.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown
        file = self.save_file(video)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=mimetypes.types_map[".mp4"],
                            file=file,
                            attributes=[
                                types.DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height
                                ),
                                types.DocumentAttributeFilename(os.path.basename(video))
                            ]
                        ),
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id(),
                        **style.parse(caption)
                    )
                )
            except FilePartMissing as e:
                self.save_file(video, file_id=file.id, file_part=e.x)
            else:
                return r

    def send_voice(self,
                   chat_id: int or str,
                   voice: str,
                   caption: str = "",
                   parse_mode: str = "",
                   duration: int = 0,
                   disable_notification: bool = None,
                   reply_to_message_id: int = None):
        """Use this method to send audio files.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            voice (:obj:`str`):
                Audio file to send.
                Pass a file path as string to send an audio file that exists on your local machine.

            caption (:obj:`str`, optional):
                Voice message caption, 0-200 characters.

            parse_mode (:obj:`str`):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            duration (:obj:`int`, optional):
                Duration of the voice message in seconds.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown
        file = self.save_file(voice)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=mimetypes.types_map.get("." + voice.split(".")[-1], "audio/mpeg"),
                            file=file,
                            attributes=[
                                types.DocumentAttributeAudio(
                                    voice=True,
                                    duration=duration
                                )
                            ]
                        ),
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id(),
                        **style.parse(caption)
                    )
                )
            except FilePartMissing as e:
                self.save_file(voice, file_id=file.id, file_part=e.x)
            else:
                return r

    def send_video_note(self,
                        chat_id: int or str,
                        video_note: str,
                        duration: int = 0,
                        length: int = 1,
                        disable_notification: bool = None,
                        reply_to_message_id: int = None):
        """Use this method to send video messages.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            video_note (:obj:`str`):
                Video note to send.
                Pass a file path as string to send a video note that exists on your local machine.

            duration (:obj:`int`, optional):
                Duration of sent video in seconds.

            length (:obj:`int`, optional):
                Video width and height.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        file = self.save_file(video_note)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=mimetypes.types_map[".mp4"],
                            file=file,
                            attributes=[
                                types.DocumentAttributeVideo(
                                    round_message=True,
                                    duration=duration,
                                    w=length,
                                    h=length
                                )
                            ]
                        ),
                        message="",
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id()
                    )
                )
            except FilePartMissing as e:
                self.save_file(video_note, file_id=file.id, file_part=e.x)
            else:
                return r

    def send_location(self,
                      chat_id: int or str,
                      latitude: float,
                      longitude: float,
                      disable_notification: bool = None,
                      reply_to_message_id: int = None):
        """Use this method to send points on the map.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            latitude (:obj:`float`):
                Latitude of the location.

            longitude (:obj:`float`):
                Longitude of the location.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.messages.SendMedia(
                peer=self.resolve_peer(chat_id),
                media=types.InputMediaGeoPoint(
                    types.InputGeoPoint(
                        latitude,
                        longitude
                    )
                ),
                message="",
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id()
            )
        )

    def send_venue(self,
                   chat_id: int or str,
                   latitude: float,
                   longitude: float,
                   title: str,
                   address: str,
                   foursquare_id: str = "",
                   disable_notification: bool = None,
                   reply_to_message_id: int = None):
        """Use this method to send information about a venue.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            latitude (:obj:`float`):
                Latitude of the venue.

            longitude (:obj:`float`):
                Longitude of the venue.

            title (:obj:`str`):
                Name of the venue.

            address (:obj:`str`):
                Address of the venue.

            foursquare_id (:obj:`str`, optional):
                Foursquare identifier of the venue.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.messages.SendMedia(
                peer=self.resolve_peer(chat_id),
                media=types.InputMediaVenue(
                    geo_point=types.InputGeoPoint(
                        lat=latitude,
                        long=longitude
                    ),
                    title=title,
                    address=address,
                    provider="",
                    venue_id=foursquare_id,
                    venue_type=""
                ),
                message="",
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id()
            )
        )

    def send_contact(self,
                     chat_id: int or str,
                     phone_number: str,
                     first_name: str,
                     last_name: str,
                     disable_notification: bool = None,
                     reply_to_message_id: int = None):
        """Use this method to send phone contacts.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            phone_number (:obj:`str`):
                Contact's phone number.

            first_name (:obj:`str`):
                Contact's first name.

            last_name (:obj:`str`):
                Contact's last name.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message.

        Returns:
             On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.messages.SendMedia(
                peer=self.resolve_peer(chat_id),
                media=types.InputMediaContact(
                    phone_number,
                    first_name,
                    last_name
                ),
                message="",
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id()
            )
        )

    def send_chat_action(self,
                         chat_id: int or str,
                         action: callable,
                         progress: int = 0):
        """Use this method when you need to tell the other party that something is happening on your side.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            action (:obj:`callable`):
                Type of action to broadcast.
                Choose one from the :class:`pyrogram.ChatAction` class,
                depending on what the user is about to receive.

            progress (:obj:`int`, optional):
                Progress of the upload process.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.messages.SetTyping(
                peer=self.resolve_peer(chat_id),
                action=action(progress=progress)
            )
        )

    def get_user_profile_photos(self,
                                user_id: int or str,
                                offset: int = 0,
                                limit: int = 100):
        """Use this method to get a list of profile pictures for a user.

        Args:
            user_id (:obj:`int` | :obj:`str`):
                Unique identifier of the target user.

            offset (:obj:`int`, optional):
                Sequential number of the first photo to be returned.
                By default, all photos are returned.

            limit (:obj:`int`, optional):
                Limits the number of photos to be retrieved.
                Values between 1—100 are accepted. Defaults to 100.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.photos.GetUserPhotos(
                user_id=self.resolve_peer(user_id),
                offset=offset,
                max_id=0,
                limit=limit
            )
        )

    def edit_message_text(self,
                          chat_id: int or str,
                          message_id: int,
                          text: str,
                          parse_mode: str = "",
                          disable_web_page_preview: bool = None):
        """Use this method to edit text messages.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            message_id (:obj:`int`):
                Message identifier in the chat specified in chat_id.

            text (:obj:`str`):
                New text of the message.

            parse_mode (:obj:`str`):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your message.
                Defaults to Markdown.

            disable_web_page_preview (:obj:`bool`, optional):
                Disables link previews for links in this message.

        Raises:
            :class:`pyrogram.Error`
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown

        return self.send(
            functions.messages.EditMessage(
                peer=self.resolve_peer(chat_id),
                id=message_id,
                no_webpage=disable_web_page_preview or None,
                **style.parse(text)
            )
        )

    def edit_message_caption(self,
                             chat_id: int or str,
                             message_id: int,
                             caption: str,
                             parse_mode: str = ""):
        """Use this method to edit captions of messages.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            message_id (:obj:`int`):
                Message identifier in the chat specified in chat_id.

            caption (:obj:`str`):
                New caption of the message.

            parse_mode (:obj:`str`):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

        Raises:
            :class:`pyrogram.Error`
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown

        return self.send(
            functions.messages.EditMessage(
                peer=self.resolve_peer(chat_id),
                id=message_id,
                **style.parse(caption)
            )
        )

    def delete_messages(self,
                        chat_id: int or str,
                        message_ids: list,
                        revoke: bool = None):
        """Use this method to delete messages, including service messages, with the following limitations:

        - A message can only be deleted if it was sent less than 48 hours ago.
        - Users can delete outgoing messages in groups and supergroups.
        - Users granted *can_post_messages* permissions can delete outgoing messages in channels.
        - If the user is an administrator of a group, it can delete any message there.
        - If the user has *can_delete_messages* permission in a supergroup or a channel, it can delete any message there.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            message_ids (:obj:`list`):
                List of identifiers of the messages to delete.

            revoke (:obj:`bool`, optional):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).

        Raises:
            :class:`pyrogram.Error`
        """
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChannel):
            return self.send(
                functions.channels.DeleteMessages(
                    channel=peer,
                    id=message_ids
                )
            )
        else:
            # TODO: Maybe "revoke" is superfluous.
            # If I want to delete a message, chances are I want it to
            # be deleted even from the other side
            return self.send(
                functions.messages.DeleteMessages(
                    id=message_ids,
                    revoke=revoke or None
                )
            )

    # TODO: Remove redundant code
    def save_file(self, path: str, file_id: int = None, file_part: int = 0):
        part_size = 512 * 1024
        file_size = os.path.getsize(path)
        file_total_parts = math.ceil(file_size / part_size)
        # is_big = True if file_size > 10 * 1024 * 1024 else False
        is_big = False  # Treat all files as not-big to have the server check for the md5 sum
        is_missing_part = True if file_id is not None else False
        file_id = file_id or self.rnd_id()
        md5_sum = md5() if not is_big and not is_missing_part else None

        session = Session(self.dc_id, self.test_mode, self.proxy, self.auth_key, self.config.api_id)
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

                    session.send(
                        (functions.upload.SaveBigFilePart if is_big else functions.upload.SaveFilePart)(
                            file_id=file_id,
                            file_part=file_part,
                            bytes=chunk,
                            file_total_parts=file_total_parts
                        )
                    )

                    if is_missing_part:
                        return

                    if not is_big:
                        md5_sum.update(chunk)

                    file_part += 1
        except Exception as e:
            log.error(e)
        else:
            return (types.InputFileBig if is_big else types.InputFile)(
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
                 version: int = 0):
        # TODO: Refine
        # TODO: Use proper file name and extension
        # TODO: Remove redundant code

        if dc_id != self.dc_id:
            exported_auth = self.send(
                functions.auth.ExportAuthorization(
                    dc_id=dc_id
                )
            )

            session = Session(
                dc_id,
                self.test_mode,
                self.proxy,
                Auth(dc_id, self.test_mode, self.proxy).create(),
                self.config.api_id
            )

            session.start()

            session.send(
                functions.auth.ImportAuthorization(
                    id=exported_auth.id,
                    bytes=exported_auth.bytes
                )
            )
        else:
            session = Session(
                dc_id,
                self.test_mode,
                self.proxy,
                self.auth_key,
                self.config.api_id
            )

            session.start()

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

        limit = 512 * 1024
        offset = 0

        try:
            r = session.send(
                functions.upload.GetFile(
                    location=location,
                    offset=offset,
                    limit=limit
                )
            )

            if isinstance(r, types.upload.File):
                with open("_".join([str(id), str(access_hash), str(version)]) + ".jpg", "wb") as f:
                    while True:
                        chunk = r.bytes

                        if not chunk:
                            break

                        f.write(chunk)
                        offset += limit

                        r = session.send(
                            functions.upload.GetFile(
                                location=location,
                                offset=offset,
                                limit=limit
                            )
                        )
            if isinstance(r, types.upload.FileCdnRedirect):
                ctr = CTR(r.encryption_key, r.encryption_iv)

                cdn_session = Session(
                    r.dc_id,
                    self.test_mode,
                    self.proxy,
                    Auth(r.dc_id, self.test_mode, self.proxy).create(),
                    self.config.api_id,
                    is_cdn=True
                )

                cdn_session.start()

                try:
                    with open("_".join([str(id), str(access_hash), str(version)]) + ".jpg", "wb") as f:
                        while True:
                            r2 = cdn_session.send(
                                functions.upload.GetCdnFile(
                                    location=location,
                                    file_token=r.file_token,
                                    offset=offset,
                                    limit=limit
                                )
                            )

                            if isinstance(r2, types.upload.CdnFileReuploadNeeded):
                                session.send(
                                    functions.upload.ReuploadCdnFile(
                                        file_token=r.file_token,
                                        request_token=r2.request_token
                                    )
                                )
                                continue
                            elif isinstance(r2, types.upload.CdnFile):
                                chunk = r2.bytes

                                if not chunk:
                                    break

                                # https://core.telegram.org/cdn#decrypting-files
                                decrypted_chunk = ctr.decrypt(chunk, offset)

                                # TODO: https://core.telegram.org/cdn#verifying-files
                                # TODO: Save to temp file, flush each chunk, rename to full if everything is ok

                                f.write(decrypted_chunk)
                                offset += limit
                except Exception as e:
                    log.error(e)
                finally:
                    cdn_session.stop()
        except Exception as e:
            log.error(e)
        else:
            return True
        finally:
            session.stop()

    def join_chat(self, chat_id: str):
        """Use this method to join a group chat or channel.

        Args:
            chat_id (:obj:`str`):
                Unique identifier for the target chat in form of *t.me/joinchat/* links or username of the target
                channel/supergroup (in the format @username).

        Raises:
            :class:`pyrogram.Error`
        """
        match = self.INVITE_LINK_RE.match(chat_id)

        if match:
            return self.send(
                functions.messages.ImportChatInvite(
                    hash=match.group(1)
                )
            )
        else:
            resolved_peer = self.send(
                functions.contacts.ResolveUsername(
                    username=chat_id.lower().strip("@")
                )
            )

            channel = InputPeerChannel(
                channel_id=resolved_peer.chats[0].id,
                access_hash=resolved_peer.chats[0].access_hash
            )

            return self.send(
                functions.channels.JoinChannel(
                    channel=channel
                )
            )

    def leave_chat(self, chat_id: int or str, delete: bool = False):
        """Use this method to leave a group chat or channel.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

            delete (:obj:`bool`, optional):
                Deletes the group chat dialog after leaving (for simple group chats, not supergroups).

        Raises:
            :class:`pyrogram.Error`
        """
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChannel):
            return self.send(
                functions.channels.LeaveChannel(
                    channel=self.resolve_peer(chat_id)
                )
            )
        elif isinstance(peer, types.InputPeerChat):
            r = self.send(
                functions.messages.DeleteChatUser(
                    chat_id=peer.chat_id,
                    user_id=types.InputPeerSelf()
                )
            )

            if delete:
                self.send(
                    functions.messages.DeleteHistory(
                        peer=peer,
                        max_id=0
                    )
                )

            return r

    def export_chat_invite_link(self, chat_id: int or str, new: bool = False):
        """Use this method to export an invite link to a supergroup or a channel.

        The user must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

            new (:obj:`bool`):
                The previous link will be deactivated and a new link will be generated.
                This is also used to create the invite link in case it doesn't exist yet.

        Returns:
            On success, the exported invite link as string is returned.

        Raises:
            :class:`pyrogram.Error`

        Note:
            If the returned link is a new one it may take a while for it to be activated.
        """
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChat):
            if new:
                return self.send(
                    functions.messages.ExportChatInvite(
                        chat_id=peer.chat_id
                    )
                ).link
            else:
                chat_full = self.send(
                    functions.messages.GetFullChat(
                        chat_id=peer.chat_id
                    )
                ).full_chat  # type: types.ChatFull

                if isinstance(chat_full.exported_invite, types.ChatInviteExported):
                    return chat_full.exported_invite.link
                else:
                    raise ChatAdminRequired
        elif isinstance(peer, types.InputPeerChannel):
            if new:
                return self.send(
                    functions.channels.ExportInvite(
                        channel=peer
                    )
                ).link
            else:
                channel_full = self.send(
                    functions.channels.GetFullChannel(
                        channel=peer
                    )
                ).full_chat  # type: types.ChannelFull

                if isinstance(channel_full.exported_invite, types.ChatInviteExported):
                    return channel_full.exported_invite.link
                else:
                    raise ChatAdminRequired

    def enable_cloud_password(self, password: str, hint: str = "", email: str = ""):
        """Use this method to enable the Two-Step Verification security feature (Cloud Password) on your account.

        This password will be asked when you log in on a new device in addition to the SMS code.

        Args:
            password (:obj:`str`):
                Your password.

            hint (:obj:`str`, optional):
                A password hint.

            email (:obj:`str`, optional):
                Recovery e-mail.

        Returns:
            True on success, False otherwise.

        Raises:
            :class:`pyrogram.Error`
        """
        r = self.send(functions.account.GetPassword())

        if isinstance(r, types.account.NoPassword):
            salt = r.new_salt + os.urandom(8)
            password_hash = sha256(salt + password.encode() + salt).digest()

            return self.send(
                functions.account.UpdatePasswordSettings(
                    current_password_hash=salt,
                    new_settings=types.account.PasswordInputSettings(
                        new_salt=salt,
                        new_password_hash=password_hash,
                        hint=hint,
                        email=email
                    )
                )
            )
        else:
            return False

    def change_cloud_password(self, current_password: str, new_password: str, new_hint: str = ""):
        """Use this method to change your Two-Step Verification password (Cloud Password) with a new one.

        Args:
            current_password (:obj:`str`):
                Your current password.

            new_password (:obj:`str`):
                Your new password.

            new_hint (:obj:`str`, optional):
                A new password hint.

        Returns:
            True on success, False otherwise.

        Raises:
            :class:`pyrogram.Error`
        """
        r = self.send(functions.account.GetPassword())

        if isinstance(r, types.account.Password):
            current_password_hash = sha256(r.current_salt + current_password.encode() + r.current_salt).digest()

            new_salt = r.new_salt + os.urandom(8)
            new_password_hash = sha256(new_salt + new_password.encode() + new_salt).digest()

            return self.send(
                functions.account.UpdatePasswordSettings(
                    current_password_hash=current_password_hash,
                    new_settings=types.account.PasswordInputSettings(
                        new_salt=new_salt,
                        new_password_hash=new_password_hash,
                        hint=new_hint
                    )
                )
            )
        else:
            return False

    def remove_cloud_password(self, password: str):
        """Use this method to turn off the Two-Step Verification security feature (Cloud Password) on your account.

        Args:
            password (:obj:`str`):
                Your current password.

        Returns:
            True on success, False otherwise.

        Raises:
            :class:`pyrogram.Error`
        """
        r = self.send(functions.account.GetPassword())

        if isinstance(r, types.account.Password):
            password_hash = sha256(r.current_salt + password.encode() + r.current_salt).digest()

            return self.send(
                functions.account.UpdatePasswordSettings(
                    current_password_hash=password_hash,
                    new_settings=types.account.PasswordInputSettings(
                        new_salt=b"",
                        new_password_hash=b"",
                        hint=""
                    )
                )
            )
        else:
            return False

    def send_media_group(self,
                         chat_id: int or str,
                         media: list,
                         disable_notification: bool = None,
                         reply_to_message_id: int = None):
        """Use this method to send a group of photos or videos as an album.
        On success, an Update containing the sent Messages is returned.

        Args:
            chat_id (:obj:`int` | :obj:`str`):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username). For your personal cloud storage (Saved Messages) you can
                simply use "me" or "self".

            media (:obj:`list`):
                A list containing either :obj:`pyrogram.InputMedia.Photo` or :obj:`pyrogram.InputMedia.Video` objects
                describing photos and videos to be sent, must include 2–10 items.

            disable_notification (:obj:`bool`, optional):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (:obj:`int`, optional):
                If the message is a reply, ID of the original message.
        """
        multi_media = []

        for i in media:
            if isinstance(i, InputMedia.Photo):
                style = self.html if i.parse_mode.lower() == "html" else self.markdown
                media = self.save_file(i.media)

                media = self.send(
                    functions.messages.UploadMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedPhoto(
                            file=media
                        )
                    )
                )

                single_media = types.InputSingleMedia(
                    media=types.InputMediaPhoto(
                        id=types.InputPhoto(
                            id=media.photo.id,
                            access_hash=media.photo.access_hash
                        )
                    ),
                    random_id=self.rnd_id(),
                    **style.parse(i.caption)
                )

                multi_media.append(single_media)
            elif isinstance(i, InputMedia.Video):
                style = self.html if i.parse_mode.lower() == "html" else self.markdown
                media = self.save_file(i.media)

                media = self.send(
                    functions.messages.UploadMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            file=media,
                            mime_type=mimetypes.types_map[".mp4"],
                            attributes=[
                                types.DocumentAttributeVideo(
                                    duration=i.duration,
                                    w=i.width,
                                    h=i.height
                                ),
                                types.DocumentAttributeFilename(os.path.basename(i.media))
                            ]
                        )
                    )
                )

                single_media = types.InputSingleMedia(
                    media=types.InputMediaDocument(
                        id=types.InputDocument(
                            id=media.document.id,
                            access_hash=media.document.access_hash
                        )
                    ),
                    random_id=self.rnd_id(),
                    **style.parse(i.caption)
                )

                multi_media.append(single_media)

        return self.send(
            functions.messages.SendMultiMedia(
                peer=self.resolve_peer(chat_id),
                multi_media=multi_media,
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id
            )
        )

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
import time
from collections import namedtuple
from configparser import ConfigParser
from hashlib import sha256, md5
from signal import signal, SIGINT, SIGTERM, SIGABRT
from threading import Event

from pyrogram.api import functions, types
from pyrogram.api.core import Object
from pyrogram.api.errors import (
    PhoneMigrate, NetworkMigrate, PhoneNumberInvalid,
    PhoneNumberUnoccupied, PhoneCodeInvalid, PhoneCodeHashEmpty,
    PhoneCodeExpired, PhoneCodeEmpty, SessionPasswordNeeded,
    PasswordHashInvalid, FloodWait, PeerIdInvalid, FilePartMissing
)
from pyrogram.api.types import (
    User, Chat, Channel,
    PeerUser, PeerChat, PeerChannel,
    Dialog, Message,
    InputPeerEmpty, InputPeerSelf,
    InputPeerUser, InputPeerChat, InputPeerChannel
)
from pyrogram.crypto import CTR
from pyrogram.extensions import Markdown
from pyrogram.session import Auth, Session

log = logging.getLogger(__name__)

Config = namedtuple("Config", ["api_id", "api_hash"])


class Client:
    """This object represents a Telegram Client.

    Args:
        session_name: Name to uniquely identify an authorized session.
        test_mode: Enable or disable log-in to testing servers.
    """

    INVITE_LINK_RE = re.compile(r"^(?:https?:\/\/)?t\.me\/joinchat\/(.+)$")
    DIALOGS_AT_ONCE = 100

    def __init__(self, session_name: str, test_mode: bool = False):
        self.session_name = session_name
        self.test_mode = test_mode

        self.dc_id = None
        self.auth_key = None
        self.user_id = None

        self.rnd_id = None

        self.peers_by_id = {}
        self.peers_by_username = {}

        self.markdown = Markdown(self.peers_by_id)

        self.config = None
        self.session = None

        self.update_handler = None
        self.is_idle = Event()

    def start(self):
        """Use this method to start the Client after creating it."""
        self.load_config()
        self.load_session(self.session_name)

        self.session = Session(self.dc_id, self.test_mode, self.auth_key, self.config.api_id)

        terms = self.session.start()

        if self.user_id is None:
            print("\n".join(terms.splitlines()), "\n")

            self.user_id = self.authorize()
            self.save_session()

        self.session.update_handler = self.update_handler
        self.rnd_id = self.session.msg_id
        self.get_dialogs()

        mimetypes.init()

    def stop(self):
        """Use this method to manually stop the Client."""
        self.session.stop()

    def signal_handler(self, *args):
        self.stop()
        self.is_idle.set()

    def idle(self, stop_signals: tuple = (SIGINT, SIGTERM, SIGABRT)):
        """Blocks the program execution until one of the signals are received,
        then gently stop the Client by closing the underlying connection.

        Args:
            stop_signals:
                Iterable containing signals the signal handler will listen to.
        """
        for s in stop_signals:
            signal(s, self.signal_handler)

        self.is_idle.wait()

    # TODO: Better update handler
    def set_update_handler(self, callback: callable):
        """Use this method to set the update handler

        Args:
            callback:
                A callback function that accepts a single argument: the update object.
        """
        self.update_handler = callback

    def send(self, data: Object):
        """Use this method to send Raw Function calls.

        This method makes possible to manually call every single Telegram API method in a low-level manner.
        Functions are listed in the **pyrogram.api.functions** package.

        Args:
            data:
                The API Scheme function filled with proper arguments.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.session.send(data)

    def authorize(self):
        while True:
            phone_number = input("Enter phone number: ")

            while True:
                confirm = input("Is \"{}\" correct? (y/n): ".format(phone_number))

                if confirm in ("y", "1"):
                    break
                elif confirm in ("n", "2"):
                    phone_number = input("Enter phone number: ")

            try:
                r = self.send(
                    functions.auth.SendCode(
                        phone_number,
                        self.config.api_id,
                        self.config.api_hash
                    )
                )
            except (PhoneMigrate, NetworkMigrate) as e:
                self.session.stop()

                self.dc_id = e.x
                self.auth_key = Auth(self.dc_id, self.test_mode).create()

                self.session = Session(self.dc_id, self.test_mode, self.auth_key, self.config.api_id)
                self.session.start()

                r = self.send(
                    functions.auth.SendCode(
                        phone_number,
                        self.config.api_id,
                        self.config.api_hash
                    )
                )
                break
            except PhoneNumberInvalid as e:
                print(e.MESSAGE)
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
            phone_code = input("Enter phone code: ")

            try:
                if phone_registered:
                    r = self.send(
                        functions.auth.SignIn(
                            phone_number,
                            phone_code_hash,
                            phone_code
                        )
                    )
                else:
                    try:
                        self.send(
                            functions.auth.SignIn(
                                phone_number,
                                phone_code_hash,
                                phone_code
                            )
                        )
                    except PhoneNumberUnoccupied:
                        pass

                    first_name = input("First name: ")
                    last_name = input("Last name: ")

                    r = self.send(
                        functions.auth.SignUp(
                            phone_number,
                            phone_code_hash,
                            phone_code,
                            first_name,
                            last_name
                        )
                    )
            except (PhoneCodeInvalid, PhoneCodeEmpty, PhoneCodeExpired, PhoneCodeHashEmpty) as e:
                print(e.MESSAGE)
            except SessionPasswordNeeded as e:
                print(e.MESSAGE)

                while True:
                    try:
                        r = self.send(functions.account.GetPassword())

                        print("Hint: {}".format(r.hint))
                        password = input("Enter password: ")  # TODO: Use getpass

                        password = r.current_salt + password.encode() + r.current_salt
                        password_hash = sha256(password).digest()

                        r = self.send(functions.auth.CheckPassword(password_hash))
                    except PasswordHashInvalid as e:
                        print(e.MESSAGE)
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
        config = ConfigParser()
        config.read("config.ini")

        self.config = Config(
            int(config["pyrogram"]["api_id"]),
            config["pyrogram"]["api_hash"]
        )

    def load_session(self, session_name):
        try:
            with open("{}.session".format(session_name)) as f:
                s = json.load(f)
        except FileNotFoundError:
            self.dc_id = 1
            self.auth_key = Auth(self.dc_id, self.test_mode).create()
        else:
            self.dc_id = s["dc_id"]
            self.test_mode = s["test_mode"]
            self.auth_key = base64.b64decode("".join(s["auth_key"]))
            self.user_id = s["user_id"]

    def save_session(self):
        auth_key = base64.b64encode(self.auth_key).decode()
        auth_key = [auth_key[i: i + 43] for i in range(0, len(auth_key), 43)]

        with open("{}.session".format(self.session_name), "w") as f:
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
        peers = []

        def parse_dialogs(d) -> int:
            oldest_date = 1 << 32

            for dialog in d.dialogs:  # type: Dialog
                # Only search for Users, Chats and Channels
                if not isinstance(dialog.peer, (PeerUser, PeerChat, PeerChannel)):
                    continue

                if isinstance(dialog.peer, PeerUser):
                    peer_type = "user"
                    peer_id = dialog.peer.user_id
                elif isinstance(dialog.peer, PeerChat):
                    peer_type = "chat"
                    peer_id = dialog.peer.chat_id
                elif isinstance(dialog.peer, PeerChannel):
                    peer_type = "channel"
                    peer_id = dialog.peer.channel_id
                else:
                    continue

                for message in d.messages:  # type: Message
                    is_this = peer_id == message.from_id or dialog.peer == message.to_id

                    if is_this:
                        for entity in (d.users if peer_type == "user" else d.chats):  # type: User or Chat or Channel
                            if entity.id == peer_id:
                                peers.append(
                                    dict(
                                        id=peer_id,
                                        access_hash=getattr(entity, "access_hash", None),
                                        type=peer_type,
                                        first_name=getattr(entity, "first_name", None),
                                        last_name=getattr(entity, "last_name", None),
                                        title=getattr(entity, "title", None),
                                        username=getattr(entity, "username", None),
                                    )
                                )

                                if message.date < oldest_date:
                                    oldest_date = message.date

                                break
                        break

            return oldest_date

        pinned_dialogs = self.send(functions.messages.GetPinnedDialogs())
        parse_dialogs(pinned_dialogs)

        dialogs = self.send(
            functions.messages.GetDialogs(
                0, 0, InputPeerEmpty(),
                self.DIALOGS_AT_ONCE, True
            )
        )

        offset_date = parse_dialogs(dialogs)
        log.info("Dialogs count: {}".format(len(peers)))

        while len(dialogs.dialogs) == self.DIALOGS_AT_ONCE:
            dialogs = self.send(
                functions.messages.GetDialogs(
                    offset_date, 0, types.InputPeerEmpty(),
                    self.DIALOGS_AT_ONCE, True
                )
            )

            offset_date = parse_dialogs(dialogs)
            log.info("Dialogs count: {}".format(len(peers)))

        for i in peers:
            peer_id = i["id"]
            peer_type = i["type"]
            peer_username = i["username"]
            peer_access_hash = i["access_hash"]

            if peer_type == "user":
                input_peer = InputPeerUser(
                    peer_id,
                    peer_access_hash
                )
            elif peer_type == "chat":
                input_peer = InputPeerChat(
                    peer_id
                )
            elif peer_type == "channel":
                input_peer = InputPeerChannel(
                    peer_id,
                    peer_access_hash
                )
            else:
                continue

            self.peers_by_id[peer_id] = input_peer

            if peer_username:
                peer_username = peer_username.lower()
                self.peers_by_username[peer_username] = input_peer

    def resolve_peer(self, chat_id: int or str):
        if chat_id in ("self", "me"):
            return InputPeerSelf()
        else:
            try:
                return (
                    self.peers_by_username[chat_id.lower().strip("@")]
                    if isinstance(chat_id, str)
                    else self.peers_by_id[chat_id]
                )
            except KeyError:
                raise PeerIdInvalid

    def get_me(self):
        """A simple method for testing the user authorization. Requires no parameters.

        Returns:
            Full information about the user in form of a **UserFull** object.

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
                     disable_web_page_preview: bool = None,
                     disable_notification: bool = None,
                     reply_to_msg_id: int = None):
        """Use this method to send text messages.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            text:
                Text of the message to be sent.

            disable_web_page_preview:
                Disables link previews for links in this message.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_msg_id:
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.messages.SendMessage(
                peer=self.resolve_peer(chat_id),
                no_webpage=disable_web_page_preview or None,
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_msg_id,
                random_id=self.rnd_id(),
                **self.markdown.parse(text)
            )
        )

    def forward_messages(self,
                         chat_id: int or str,
                         from_chat_id: int or str,
                         message_ids: list,
                         disable_notification: bool = None):
        """Use this method to forward messages of any kind.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            from_chat_id:
                Unique identifier for the chat where the original message was sent
                (or channel username in the format @channelusername).

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            message_ids:
                A list of Message identifiers in the chat specified in *from_chat_id*.

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
                   ttl_seconds: int = None,
                   disable_notification: bool = None,
                   reply_to_message_id: int = None):
        """Use this method to send photos.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            photo:
                Photo to send.
                Pass a file path as string to send a photo that exists on your local machine.

            caption:
                Photo caption, 0-200 characters.

            ttl_seconds:
                Self-Destruct Timer.
                If you set a timer, the photo will self-destruct after it was viewed.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id:
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        file = self.save_file(photo)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedPhoto(
                            file=file,
                            caption=caption,
                            ttl_seconds=ttl_seconds
                        ),
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id()
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
                   duration: int = 0,
                   performer: str = None,
                   title: str = None,
                   disable_notification: bool = None,
                   reply_to_message_id: int = None):
        """Use this method to send audio files.

        For sending voice messages, use the **send_voice** method instead.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            audio:
                Audio file to send.
                Pass a file path as string to send an audio file that exists on your local machine.

            caption:
                Audio caption, 0-200 characters.

            duration:
                Duration of the audio in seconds.

            performer:
                Performer.

            title:
                Track name.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id:
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        file = self.save_file(audio)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=mimetypes.types_map.get("." + audio.split(".")[-1], "audio/mpeg"),
                            file=file,
                            caption=caption,
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
                        random_id=self.rnd_id()
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
                      disable_notification: bool = None,
                      reply_to_message_id: int = None):
        """Use this method to send general files.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            document:
                File to send.
                Pass a file path as string to send a file that exists on your local machine.

            caption:
                Document caption, 0-200 characters.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id:
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        file = self.save_file(document)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=mimetypes.types_map.get("." + document.split(".")[-1], "text/plain"),
                            file=file,
                            caption=caption,
                            attributes=[
                                types.DocumentAttributeFilename(os.path.basename(document))
                            ]
                        ),
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id()
                    )
                )
            except FilePartMissing as e:
                self.save_file(document, file_id=file.id, file_part=e.x)
            else:
                return r

    def send_video(self,
                   chat_id: int or str,
                   video: str,
                   duration: int = 0,
                   width: int = 0,
                   height: int = 0,
                   caption: str = "",
                   disable_notification: bool = None,
                   reply_to_message_id: int = None):
        """Use this method to send video files.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            video:
                Video to send.
                Pass a file path as string to send a video that exists on your local machine.

            duration:
                Duration of sent video in seconds.

            width:
                Video width.

            height:
                Video height.

            caption:
                Video caption, 0-200 characters.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id:
                If the message is a reply, ID of the original message.

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        file = self.save_file(video)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=mimetypes.types_map[".mp4"],
                            file=file,
                            caption=caption,
                            attributes=[
                                types.DocumentAttributeVideo(
                                    duration=duration,
                                    w=width,
                                    h=height
                                )
                            ]
                        ),
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id()
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
                   duration: int = 0,
                   disable_notification: bool = None,
                   reply_to_message_id: int = None):
        """Use this method to send audio files.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            voice:
                Audio file to send.
                Pass a file path as string to send an audio file that exists on your local machine.

            caption:
                Voice message caption, 0-200 characters.

            duration:
                Duration of the voice message in seconds.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id:
                If the message is a reply, ID of the original message

        Returns:
            On success, the sent Message is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        file = self.save_file(voice)

        while True:
            try:
                r = self.send(
                    functions.messages.SendMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=mimetypes.types_map.get("." + voice.split(".")[-1], "audio/mpeg"),
                            file=file,
                            caption=caption,
                            attributes=[
                                types.DocumentAttributeAudio(
                                    voice=True,
                                    duration=duration
                                )
                            ]
                        ),
                        silent=disable_notification or None,
                        reply_to_msg_id=reply_to_message_id,
                        random_id=self.rnd_id()
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
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            video_note:
                Video note to send.
                Pass a file path as string to send a video note that exists on your local machine.

            duration:
                Duration of sent video in seconds.

            length:
                Video width and height.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id:
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
                            caption="",
                            attributes=[
                                types.DocumentAttributeVideo(
                                    round_message=True,
                                    duration=duration,
                                    w=length,
                                    h=length
                                )
                            ]
                        ),
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
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            latitude:
                Latitude of the location.

            longitude:
                Longitude of the location.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id:
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
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            latitude:
                Latitude of the venue.

            longitude:
                Longitude of the venue.

            title:
                Name of the venue.

            address:
                Address of the venue.

            foursquare_id:
                Foursquare identifier of the venue.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id:
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
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            phone_number:
                Contact's phone number.

            first_name:
                Contact's first name.

            last_name:
                Contact's last name.

            disable_notification:
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id:
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
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            action:
                Type of action to broadcast.
                Choose one from the :class:`pyrogram.ChatAction` class,
                depending on what the user is about to receive.

            progress:
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
            user_id:
                Unique identifier of the target user.

            offset:
                Sequential number of the first photo to be returned.
                By default, all photos are returned.

            limit:
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
                          disable_web_page_preview: bool = None):
        """Use this method to edit text messages.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            message_id:
                Message identifier in the chat specified in chat_id.

            text:
                New text of the message.

            disable_web_page_preview:
                Disables link previews for links in this message.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.messages.EditMessage(
                peer=self.resolve_peer(chat_id),
                id=message_id,
                no_webpage=disable_web_page_preview or None,
                **self.markdown.parse(text)
            )
        )

    def edit_message_caption(self,
                             chat_id: int or str,
                             message_id: int,
                             caption: str):
        """Use this method to edit captions of messages.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            message_id:
                Message identifier in the chat specified in chat_id.

            caption:
                New caption of the message.

        Raises:
            :class:`pyrogram.Error`
        """
        return self.send(
            functions.messages.EditMessage(
                peer=self.resolve_peer(chat_id),
                id=message_id,
                message=caption
            )
        )

    def delete_messages(self,
                        message_ids: list,
                        revoke: bool = None):
        """Use this method to delete messages, including service messages, with the following limitations:

        - A message can only be deleted if it was sent less than 48 hours ago.
        - Users can delete outgoing messages in groups and supergroups.
        - Users granted *can_post_messages* permissions can delete outgoing messages in channels.
        - If the user is an administrator of a group, it can delete any message there.
        - If the user has *can_delete_messages* permission in a supergroup or a channel, it can delete any message there.

        Args:
            message_ids:
                List of identifiers of the messages to delete.

            revoke:
                Deletes messages on both parts (for private chats).

        Raises:
            :class:`pyrogram.Error`
        """
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

        session = Session(self.dc_id, self.test_mode, self.auth_key, self.config.api_id)
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
                Auth(dc_id, self.test_mode).create(),
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
                    Auth(r.dc_id, self.test_mode).create(),
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
            chat_id:
                Unique identifier for the target chat in form of *t.me/joinchat/* links or username of the target
                channel (in the format @channelusername)

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
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

            delete:
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

    def export_chat_invite_link(self, chat_id: int or str):
        """Use this method to export an invite link to a supergroup or a channel.

        The user must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Args:
            chat_id:
                Unique identifier for the target chat or username of the target channel
                (in the format @channelusername).

        Returns:
            On success, the exported invite link as string is returned.

        Raises:
            :class:`pyrogram.Error`
        """
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChat):
            return self.send(
                functions.messages.ExportChatInvite(
                    chat_id=peer.chat_id
                )
            ).link
        elif isinstance(peer, types.InputPeerChannel):
            return self.send(
                functions.channels.ExportInvite(
                    channel=peer
                )
            ).link

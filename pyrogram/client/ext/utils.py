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
import base64
import struct
import sys
from concurrent.futures.thread import ThreadPoolExecutor
from typing import List
from typing import Union

import pyrogram
from pyrogram.api.types import PeerUser, PeerChat, PeerChannel
from . import BaseClient
from ...api import types


def decode_file_id(s: str) -> bytes:
    s = base64.urlsafe_b64decode(s + "=" * (-len(s) % 4))
    r = b""

    try:
        assert s[-1] == 2
        skip = 1
    except AssertionError:
        assert s[-2] == 22
        assert s[-1] == 4
        skip = 2

    i = 0

    while i < len(s) - skip:
        if s[i] != 0:
            r += bytes([s[i]])
        else:
            r += b"\x00" * s[i + 1]
            i += 1

        i += 1

    return r


def encode_file_id(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([22]) + bytes([4]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return base64.urlsafe_b64encode(r).decode().rstrip("=")


def encode_file_ref(file_ref: bytes) -> str:
    return base64.urlsafe_b64encode(file_ref).decode().rstrip("=")


def decode_file_ref(file_ref: str) -> bytes:
    if file_ref is None:
        return b""

    return base64.urlsafe_b64decode(file_ref + "=" * (-len(file_ref) % 4))


async def ainput(prompt: str = ""):
    print(prompt, end="", flush=True)

    with ThreadPoolExecutor(1) as executor:
        return (await asyncio.get_event_loop().run_in_executor(
            executor, sys.stdin.readline
        )).rstrip()


def get_offset_date(dialogs):
    for m in reversed(dialogs.messages):
        if isinstance(m, types.MessageEmpty):
            continue
        else:
            return m.date
    else:
        return 0


def get_input_media_from_file_id(
    file_id_str: str,
    file_ref: str = None,
    expected_media_type: int = None
) -> Union[types.InputMediaPhoto, types.InputMediaDocument]:
    try:
        decoded = decode_file_id(file_id_str)
    except Exception:
        raise ValueError("Failed to decode file_id: {}".format(file_id_str))
    else:
        media_type = decoded[0]

        if expected_media_type is not None:
            if media_type != expected_media_type:
                media_type_str = BaseClient.MEDIA_TYPE_ID.get(media_type, None)
                expected_media_type_str = BaseClient.MEDIA_TYPE_ID.get(expected_media_type, None)

                raise ValueError(
                    'Expected: "{}", got "{}" file_id instead'.format(expected_media_type_str, media_type_str)
                )

        if media_type in (0, 1, 14):
            raise ValueError("This file_id can only be used for download: {}".format(file_id_str))

        if media_type == 2:
            unpacked = struct.unpack("<iiqqqiiii", decoded)
            dc_id, file_id, access_hash, volume_id, _, _, type, local_id = unpacked[1:]

            return types.InputMediaPhoto(
                id=types.InputPhoto(
                    id=file_id,
                    access_hash=access_hash,
                    file_reference=decode_file_ref(file_ref)
                )
            )

        if media_type in (3, 4, 5, 8, 9, 10, 13):
            unpacked = struct.unpack("<iiqq", decoded)
            dc_id, file_id, access_hash = unpacked[1:]

            return types.InputMediaDocument(
                id=types.InputDocument(
                    id=file_id,
                    access_hash=access_hash,
                    file_reference=decode_file_ref(file_ref)
                )
            )

        raise ValueError("Unknown media type: {}".format(file_id_str))


async def parse_messages(client, messages: types.messages.Messages, replies: int = 1) -> List["pyrogram.Message"]:
    users = {i.id: i for i in messages.users}
    chats = {i.id: i for i in messages.chats}

    if not messages.messages:
        return pyrogram.List()

    parsed_messages = []

    for message in messages.messages:
        parsed_messages.append(await pyrogram.Message._parse(client, message, users, chats, replies=0))

    if replies:
        messages_with_replies = {i.id: getattr(i, "reply_to_msg_id", None) for i in messages.messages}
        reply_message_ids = [i[0] for i in filter(lambda x: x[1] is not None, messages_with_replies.items())]

        if reply_message_ids:
            reply_messages = await client.get_messages(
                parsed_messages[0].chat.id,
                reply_to_message_ids=reply_message_ids,
                replies=replies - 1
            )

            for message in parsed_messages:
                reply_id = messages_with_replies[message.message_id]

                for reply in reply_messages:
                    if reply.message_id == reply_id:
                        message.reply_to_message = reply

    return pyrogram.List(parsed_messages)


def parse_deleted_messages(client, update) -> List["pyrogram.Message"]:
    messages = update.messages
    channel_id = getattr(update, "channel_id", None)

    parsed_messages = []

    for message in messages:
        parsed_messages.append(
            pyrogram.Message(
                message_id=message,
                chat=pyrogram.Chat(
                    id=get_channel_id(channel_id),
                    type="channel",
                    client=client
                ) if channel_id is not None else None,
                client=client
            )
        )

    return pyrogram.List(parsed_messages)


def unpack_inline_message_id(inline_message_id: str) -> types.InputBotInlineMessageID:
    r = inline_message_id + "=" * (-len(inline_message_id) % 4)
    r = struct.unpack("<iqq", base64.b64decode(r, altchars="-_"))

    return types.InputBotInlineMessageID(
        dc_id=r[0],
        id=r[1],
        access_hash=r[2]
    )


MIN_CHANNEL_ID = -1002147483647
MAX_CHANNEL_ID = -1000000000000
MIN_CHAT_ID = -2147483647
MAX_USER_ID = 2147483647


def get_peer_id(peer: Union[PeerUser, PeerChat, PeerChannel]) -> int:
    if isinstance(peer, PeerUser):
        return peer.user_id

    if isinstance(peer, PeerChat):
        return -peer.chat_id

    if isinstance(peer, PeerChannel):
        return MAX_CHANNEL_ID - peer.channel_id

    raise ValueError("Peer type invalid: {}".format(peer))


def get_peer_type(peer_id: int) -> str:
    if peer_id < 0:
        if MIN_CHAT_ID <= peer_id:
            return "chat"

        if MIN_CHANNEL_ID <= peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"

    raise ValueError("Peer id invalid: {}".format(peer_id))


def get_channel_id(peer_id: int) -> int:
    return MAX_CHANNEL_ID - peer_id

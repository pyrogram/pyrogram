#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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
import base64
import functools
import hashlib
import os
import struct
from concurrent.futures.thread import ThreadPoolExecutor
from datetime import datetime, timezone
from getpass import getpass
import re
from typing import Union, List, Dict, Optional

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram.errors import AuthBytesInvalid
from pyrogram.file_id import FileId, FileType, PHOTO_TYPES, DOCUMENT_TYPES
from pyrogram.session import Session
from pyrogram.session.auth import Auth


async def ainput(prompt: str = "", *, hide: bool = False):
    """Just like the built-in input, but async"""
    with ThreadPoolExecutor(1) as executor:
        func = functools.partial(getpass if hide else input, prompt)
        return await asyncio.get_event_loop().run_in_executor(executor, func)


def get_input_media_from_file_id(
    file_id: str,
    expected_file_type: FileType = None,
    ttl_seconds: int = None,
    has_spoiler: bool = None
) -> Union["raw.types.InputMediaPhoto", "raw.types.InputMediaDocument"]:
    try:
        decoded = FileId.decode(file_id)
    except Exception:
        raise ValueError(
            f'Failed to decode "{file_id}". The value does not represent an existing local file, '
            f"HTTP URL, or valid file id."
        )

    file_type = decoded.file_type

    if expected_file_type is not None and file_type != expected_file_type:
        raise ValueError(f"Expected {expected_file_type.name}, got {file_type.name} file id instead")

    if file_type in (FileType.THUMBNAIL, FileType.CHAT_PHOTO):
        raise ValueError(f"This file id can only be used for download: {file_id}")

    if file_type in PHOTO_TYPES:
        return raw.types.InputMediaPhoto(
            id=raw.types.InputPhoto(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference
            ),
            spoiler=has_spoiler,
            ttl_seconds=ttl_seconds
        )

    if file_type in DOCUMENT_TYPES:
        return raw.types.InputMediaDocument(
            id=raw.types.InputDocument(
                id=decoded.media_id,
                access_hash=decoded.access_hash,
                file_reference=decoded.file_reference
            ),
            spoiler=has_spoiler,
            ttl_seconds=ttl_seconds
        )

    raise ValueError(f"Unknown file id: {file_id}")


async def parse_messages(
    client,
    messages: "raw.types.messages.Messages",
    replies: int = 1,
    business_connection_id: str = None
) -> List["types.Message"]:
    users = {i.id: i for i in messages.users}
    chats = {i.id: i for i in messages.chats}
    topics = {i.id: i for i in messages.topics} if hasattr(messages, "topics") else None

    if not messages.messages:
        return types.List()

    parsed_messages = []

    for message in messages.messages:
        parsed_messages.append(
            await types.Message._parse(
                client,
                message,
                users,
                chats,
                topics,
                replies=0,
                business_connection_id=business_connection_id
            )
        )

    if replies:
        messages_with_replies = {
            i.id: i.reply_to
            for i in messages.messages
            if not isinstance(i, raw.types.MessageEmpty) and i.reply_to and isinstance(i.reply_to, raw.types.MessageReplyHeader)
        }

        message_reply_to_story = {
            i.id: {'user_id': i.reply_to.user_id, 'story_id': i.reply_to.story_id}
            for i in messages.messages
            if not isinstance(i, raw.types.MessageEmpty) and i.reply_to and isinstance(i.reply_to, raw.types.MessageReplyStoryHeader)
        }

        if messages_with_replies:
            # We need a chat id, but some messages might be empty (no chat attribute available)
            # Scan until we find a message with a chat available (there must be one, because we are fetching replies)
            for m in parsed_messages:
                if not isinstance(m, types.Message):
                    continue

                if m.chat:
                    chat_id = m.chat.id
                    break
            else:
                chat_id = 0

            is_all_within_chat = not any(
                value.reply_to_peer_id
                for value in messages_with_replies.values()
            )
            reply_messages: List[pyrogram.types.Message] = []
            if is_all_within_chat:
                # fast path: fetch all messages within the same chat
                reply_messages = await client.get_messages(
                    chat_id,
                    reply_to_message_ids=messages_with_replies.keys(),
                    replies=replies - 1
                )
            else:
                # slow path: fetch all messages individually
                for target_reply_to in messages_with_replies.values():
                    to_be_added_msg = None
                    the_chat_id = chat_id
                    if target_reply_to.reply_to_peer_id:
                        the_chat_id = get_channel_id(target_reply_to.reply_to_peer_id.channel_id)
                    to_be_added_msg = await client.get_messages(
                        chat_id=the_chat_id,
                        message_ids=target_reply_to.reply_to_msg_id,
                        replies=replies - 1
                    )
                    if isinstance(to_be_added_msg, list):
                        for current_to_be_added in to_be_added_msg:
                            reply_messages.append(current_to_be_added)
                    elif to_be_added_msg:
                        reply_messages.append(to_be_added_msg)

            for message in parsed_messages:
                reply_to = messages_with_replies.get(message.id, None)
                if not reply_to:
                    continue

                reply_id = reply_to.reply_to_msg_id

                for reply in reply_messages:
                    if reply.id == reply_id and not reply.forum_topic_created:
                        message.reply_to_message = reply

        if message_reply_to_story:
            for m in parsed_messages:
                if not isinstance(m, types.Message):
                    continue

                if m.chat:
                    chat_id = m.chat.id
                    break
            else:
                chat_id = 0

            reply_messages = {}
            for msg_id in message_reply_to_story:
                reply_messages[msg_id] = await client.get_stories(
                    message_reply_to_story[msg_id]['user_id'],
                    message_reply_to_story[msg_id]['story_id']
                )

            for message in parsed_messages:
                if message.id in reply_messages:
                    message.reply_to_story = reply_messages[message.id]

    return types.List(parsed_messages)


def parse_deleted_messages(client, update, users, chats) -> List["types.Message"]:
    messages = update.messages
    channel_id = getattr(update, "channel_id", None)
    business_connection_id = getattr(update, "connection_id", None)
    peer = getattr(update, "peer", None)

    chat = None

    if channel_id:
        chat = types.Chat(
            id=get_channel_id(channel_id),
            type=enums.ChatType.CHANNEL,
            client=client
        )
    if peer:
        chat_id = get_raw_peer_id(peer)
        if chat_id:
            if isinstance(peer, raw.types.PeerUser):
                chat = types.Chat._parse_user_chat(client, users[chat_id])

            elif isinstance(peer, raw.types.PeerChat):
                chat = types.Chat._parse_chat_chat(client, chats[chat_id])

            else:
                chat = types.Chat._parse_channel_chat(
                    client, chats[chat_id]
                )

    parsed_messages = []

    for message in messages:
        parsed_messages.append(
            types.Message(
                id=message,
                chat=chat,
                business_connection_id=business_connection_id,
                client=client
            )
        )

    return types.List(parsed_messages)


def pack_inline_message_id(msg_id: "raw.base.InputBotInlineMessageID"):
    if isinstance(msg_id, raw.types.InputBotInlineMessageID):
        inline_message_id_packed = struct.pack(
            "<iqq",
            msg_id.dc_id,
            msg_id.id,
            msg_id.access_hash
        )
    else:
        inline_message_id_packed = struct.pack(
            "<iqiq",
            msg_id.dc_id,
            msg_id.owner_id,
            msg_id.id,
            msg_id.access_hash
        )

    return base64.urlsafe_b64encode(inline_message_id_packed).decode().rstrip("=")


def unpack_inline_message_id(inline_message_id: str) -> "raw.base.InputBotInlineMessageID":
    padded = inline_message_id + "=" * (-len(inline_message_id) % 4)
    decoded = base64.urlsafe_b64decode(padded)

    if len(decoded) == 20:
        unpacked = struct.unpack("<iqq", decoded)

        return raw.types.InputBotInlineMessageID(
            dc_id=unpacked[0],
            id=unpacked[1],
            access_hash=unpacked[2]
        )
    else:
        unpacked = struct.unpack("<iqiq", decoded)

        return raw.types.InputBotInlineMessageID64(
            dc_id=unpacked[0],
            owner_id=unpacked[1],
            id=unpacked[2],
            access_hash=unpacked[3]
        )


MIN_CHANNEL_ID = -1002147483647
MAX_CHANNEL_ID = -1000000000000
MIN_CHAT_ID = -999999999999
MAX_USER_ID_OLD = 2147483647
MAX_USER_ID = 999999999999


def get_raw_peer_id(peer: Union[raw.base.Peer, raw.base.InputPeer]) -> Optional[int]:
    """Get the raw peer id from a Peer object"""
    if isinstance(peer, (raw.types.PeerUser, raw.types.InputPeerUser)):
        return peer.user_id

    if isinstance(peer, (raw.types.PeerChat, raw.types.InputPeerChat)):
        return peer.chat_id

    if isinstance(peer, (raw.types.PeerChannel, raw.types.InputPeerChannel)):
        return peer.channel_id

    return None


def get_peer_id(peer: Union[raw.base.Peer, raw.base.InputPeer]) -> int:
    """Get the non-raw peer id from a Peer object"""
    if isinstance(peer, (raw.types.PeerUser, raw.types.InputPeerUser)):
        return peer.user_id

    if isinstance(peer, (raw.types.PeerChat, raw.types.InputPeerChat)):
        return -peer.chat_id

    if isinstance(peer, (raw.types.PeerChannel, raw.types.InputPeerChannel)):
        return MAX_CHANNEL_ID - peer.channel_id

    raise ValueError(f"Peer type invalid: {peer}")


def get_peer_type(peer_id: int) -> str:
    if peer_id < 0:
        if MIN_CHAT_ID <= peer_id:
            return "chat"

        if MIN_CHANNEL_ID <= peer_id < MAX_CHANNEL_ID:
            return "channel"
    elif 0 < peer_id <= MAX_USER_ID:
        return "user"

    raise ValueError(f"Peer id invalid: {peer_id}")


def get_reply_to(
    reply_to_message_id: Optional[int] = None,
    message_thread_id: Optional[int] = None,
    reply_to_peer: Optional[raw.base.InputPeer] = None,
    quote_text: Optional[str] = None,
    quote_entities: Optional[List[raw.base.MessageEntity]] = None,
    quote_offset: Optional[int] = None,
    reply_to_story_id: Optional[int] = None
) -> Optional[Union[raw.types.InputReplyToMessage, raw.types.InputReplyToStory]]:
    """Get InputReply for reply_to argument"""
    if all((reply_to_peer, reply_to_story_id)):
        return raw.types.InputReplyToStory(peer=reply_to_peer, story_id=reply_to_story_id)  # type: ignore[arg-type]

    if any((reply_to_message_id, message_thread_id)):
        return raw.types.InputReplyToMessage(
            reply_to_msg_id=reply_to_message_id or message_thread_id,  # type: ignore[arg-type]
            top_msg_id=message_thread_id if reply_to_message_id else None,
            reply_to_peer_id=reply_to_peer,
            quote_text=quote_text,
            quote_entities=quote_entities,
            quote_offset=quote_offset,
        )

    return None


def get_channel_id(peer_id: int) -> int:
    return MAX_CHANNEL_ID - peer_id


def btoi(b: bytes) -> int:
    return int.from_bytes(b, "big")


def itob(i: int) -> bytes:
    return i.to_bytes(256, "big")


def sha256(data: bytes) -> bytes:
    return hashlib.sha256(data).digest()


def xor(a: bytes, b: bytes) -> bytes:
    return bytes(i ^ j for i, j in zip(a, b))


def compute_password_hash(
    algo: raw.types.PasswordKdfAlgoSHA256SHA256PBKDF2HMACSHA512iter100000SHA256ModPow,
    password: str
) -> bytes:
    hash1 = sha256(algo.salt1 + password.encode() + algo.salt1)
    hash2 = sha256(algo.salt2 + hash1 + algo.salt2)
    hash3 = hashlib.pbkdf2_hmac("sha512", hash2, algo.salt1, 100000)

    return sha256(algo.salt2 + hash3 + algo.salt2)


# noinspection PyPep8Naming
def compute_password_check(
    r: raw.types.account.Password,
    password: str
) -> raw.types.InputCheckPasswordSRP:
    algo = r.current_algo

    p_bytes = algo.p
    p = btoi(algo.p)

    g_bytes = itob(algo.g)
    g = algo.g

    B_bytes = r.srp_B
    B = btoi(B_bytes)

    srp_id = r.srp_id

    x_bytes = compute_password_hash(algo, password)
    x = btoi(x_bytes)

    g_x = pow(g, x, p)

    k_bytes = sha256(p_bytes + g_bytes)
    k = btoi(k_bytes)

    kg_x = (k * g_x) % p

    while True:
        a_bytes = os.urandom(256)
        a = btoi(a_bytes)

        A = pow(g, a, p)
        A_bytes = itob(A)

        u = btoi(sha256(A_bytes + B_bytes))

        if u > 0:
            break

    g_b = (B - kg_x) % p

    ux = u * x
    a_ux = a + ux
    S = pow(g_b, a_ux, p)
    S_bytes = itob(S)

    K_bytes = sha256(S_bytes)

    M1_bytes = sha256(
        xor(sha256(p_bytes), sha256(g_bytes))
        + sha256(algo.salt1)
        + sha256(algo.salt2)
        + A_bytes
        + B_bytes
        + K_bytes
    )

    return raw.types.InputCheckPasswordSRP(srp_id=srp_id, A=A_bytes, M1=M1_bytes)


async def parse_text_entities(
    client: "pyrogram.Client",
    text: str,
    parse_mode: enums.ParseMode,
    entities: List["types.MessageEntity"]
) -> Dict[str, Union[str, List[raw.base.MessageEntity]]]:
    if entities:
        # Inject the client instance because parsing user mentions requires it
        for entity in entities:
            entity._client = client

        text, entities = text, [await entity.write() for entity in entities] or None
    else:
        text, entities = (await client.parser.parse(text, parse_mode)).values()

    return {
        "message": text,
        "entities": entities
    }


def zero_datetime() -> datetime:
    return datetime.fromtimestamp(0, timezone.utc)


def max_datetime() -> datetime:
    return datetime.fromtimestamp((1 << 31) - 1, timezone.utc)


def timestamp_to_datetime(ts: Optional[int]) -> Optional[datetime]:
    return datetime.fromtimestamp(ts) if ts else None


def datetime_to_timestamp(dt: Optional[datetime]) -> Optional[int]:
    return int(dt.timestamp()) if dt else None


def get_first_url(text):
    text = re.sub(r"^\s*(<[\w<>=\s\"]*>)\s*", r"\1", text)
    text = re.sub(r"\s*(</[\w</>]*>)\s*$", r"\1", text)

    matches = re.findall(r"(https?):\/\/([\w_-]+(?:(?:\.[\w_-]+)+))([\w.,@?^=%&:\/~+#-]*[\w@?^=%&\/~+#-])", text)

    return f"{matches[0][0]}://{matches[0][1]}{matches[0][2]}" if matches else None

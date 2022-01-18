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

import bisect
from hashlib import sha256
from io import BytesIO
from os import urandom
from typing import List

from pyrogram.errors import SecurityCheckMismatch
from pyrogram.raw.core import Message, Long
from . import aes
from ..session.internals import MsgId

STORED_MSG_IDS_MAX_SIZE = 1000 * 2


def kdf(auth_key: bytes, msg_key: bytes, outgoing: bool) -> tuple:
    # https://core.telegram.org/mtproto/description#defining-aes-key-and-initialization-vector
    x = 0 if outgoing else 8

    sha256_a = sha256(msg_key + auth_key[x: x + 36]).digest()
    sha256_b = sha256(auth_key[x + 40:x + 76] + msg_key).digest()  # 76 = 40 + 36

    aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
    aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]

    return aes_key, aes_iv


def pack(message: Message, salt: int, session_id: bytes, auth_key: bytes, auth_key_id: bytes) -> bytes:
    data = Long(salt) + session_id + message.write()
    padding = urandom(-(len(data) + 12) % 16 + 12)

    # 88 = 88 + 0 (outgoing message)
    msg_key_large = sha256(auth_key[88: 88 + 32] + data + padding).digest()
    msg_key = msg_key_large[8:24]
    aes_key, aes_iv = kdf(auth_key, msg_key, True)

    return auth_key_id + msg_key + aes.ige256_encrypt(data + padding, aes_key, aes_iv)


def unpack(
    b: BytesIO,
    session_id: bytes,
    auth_key: bytes,
    auth_key_id: bytes,
    stored_msg_ids: List[int]
) -> Message:
    SecurityCheckMismatch.check(b.read(8) == auth_key_id)

    msg_key = b.read(16)
    aes_key, aes_iv = kdf(auth_key, msg_key, False)
    data = BytesIO(aes.ige256_decrypt(b.read(), aes_key, aes_iv))
    data.read(8)  # Salt

    # https://core.telegram.org/mtproto/security_guidelines#checking-session-id
    SecurityCheckMismatch.check(data.read(8) == session_id)

    try:
        message = Message.read(data)
    except KeyError as e:
        if e.args[0] == 0:
            raise ConnectionError(f"Received empty data. Check your internet connection.")

        left = data.read().hex()

        left = [left[i:i + 64] for i in range(0, len(left), 64)]
        left = [[left[i:i + 8] for i in range(0, len(left), 8)] for left in left]
        left = "\n".join(" ".join(x for x in left) for left in left)

        raise ValueError(f"The server sent an unknown constructor: {hex(e.args[0])}\n{left}")

    # https://core.telegram.org/mtproto/security_guidelines#checking-sha256-hash-value-of-msg-key
    # 96 = 88 + 8 (incoming message)
    SecurityCheckMismatch.check(msg_key == sha256(auth_key[96:96 + 32] + data.getvalue()).digest()[8:24])

    # https://core.telegram.org/mtproto/security_guidelines#checking-message-length
    data.seek(32)  # Get to the payload, skip salt (8) + session_id (8) + msg_id (8) + seq_no (4) + length (4)
    payload = data.read()
    padding = payload[message.length:]
    SecurityCheckMismatch.check(12 <= len(padding) <= 1024)
    SecurityCheckMismatch.check(len(payload) % 4 == 0)

    # https://core.telegram.org/mtproto/security_guidelines#checking-msg-id
    SecurityCheckMismatch.check(message.msg_id % 2 != 0)

    if len(stored_msg_ids) > STORED_MSG_IDS_MAX_SIZE:
        del stored_msg_ids[:STORED_MSG_IDS_MAX_SIZE // 2]

    if stored_msg_ids:
        # Ignored message: msg_id is lower than all of the stored values
        if message.msg_id < stored_msg_ids[0]:
            raise SecurityCheckMismatch

        # Ignored message: msg_id is equal to any of the stored values
        if message.msg_id in stored_msg_ids:
            raise SecurityCheckMismatch

        time_diff = (message.msg_id - MsgId()) / 2 ** 32

        # Ignored message: msg_id belongs over 30 seconds in the future
        if time_diff > 30:
            raise SecurityCheckMismatch

        # Ignored message: msg_id belongs over 300 seconds in the past
        if time_diff < -300:
            raise SecurityCheckMismatch

    bisect.insort(stored_msg_ids, message.msg_id)

    return message

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

from base64 import b64decode, b64encode

from ...api import types


def decode(s: str) -> bytes:
    s = b64decode(s + "=" * (-len(s) % 4), "-_")
    r = b""

    assert s[-1] == 2

    i = 0
    while i < len(s) - 1:
        if s[i] != 0:
            r += bytes([s[i]])
        else:
            r += b"\x00" * s[i + 1]
            i += 1

        i += 1

    return r


def encode(s: bytes) -> str:
    r = b""
    n = 0

    for i in s + bytes([2]):
        if i == 0:
            n += 1
        else:
            if n:
                r += b"\x00" + bytes([n])
                n = 0

            r += bytes([i])

    return b64encode(r, b"-_").decode().rstrip("=")


def get_peer_id(input_peer) -> int:
    return (
        input_peer.user_id if isinstance(input_peer, types.InputPeerUser)
        else -input_peer.chat_id if isinstance(input_peer, types.InputPeerChat)
        else int("-100" + str(input_peer.channel_id))
    )


def get_input_peer(peer_id: int, access_hash: int):
    return (
        types.InputPeerUser(peer_id, access_hash) if peer_id > 0
        else types.InputPeerChannel(int(str(peer_id)[4:]), access_hash)
        if (str(peer_id).startswith("-100") and access_hash)
        else types.InputPeerChat(-peer_id)
    )


def get_offset_date(dialogs):
    for m in reversed(dialogs.messages):
        if isinstance(m, types.MessageEmpty):
            continue
        else:
            return m.date
    else:
        return 0

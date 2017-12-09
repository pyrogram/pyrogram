# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017 Dan Tès <https://github.com/delivrance>
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

from hashlib import sha1, sha256


class KDF:
    def __new__(cls, auth_key: bytes, msg_key: bytes, outgoing: bool) -> tuple:
        # https://core.telegram.org/mtproto/description#defining-aes-key-and-initialization-vector
        x = 0 if outgoing else 8

        sha1_a = sha1(msg_key + auth_key[x:x + 32]).digest()
        sha1_b = sha1(auth_key[x + 32:x + 48] + msg_key + auth_key[x + 48:x + 64]).digest()
        sha1_c = sha1(auth_key[x + 64:x + 96] + msg_key).digest()
        sha1_d = sha1(msg_key + auth_key[x + 96:x + 128]).digest()

        aes_key = sha1_a[:8] + sha1_b[8:20] + sha1_c[4:16]
        aes_iv = sha1_a[8:20] + sha1_b[:8] + sha1_c[16:20] + sha1_d[:8]

        return aes_key, aes_iv


class KDF2:
    def __new__(cls, auth_key: bytes, msg_key: bytes, outgoing: bool) -> tuple:
        # https://core.telegram.org/mtproto/description#defining-aes-key-and-initialization-vector
        x = 0 if outgoing else 8

        sha256_a = sha256(msg_key + auth_key[x: x + 36]).digest()
        sha256_b = sha256(auth_key[x + 40:x + 76] + msg_key).digest()  # 76 = 40 + 36

        aes_key = sha256_a[:8] + sha256_b[8:24] + sha256_a[24:32]
        aes_iv = sha256_b[:8] + sha256_a[8:24] + sha256_b[24:32]

        return aes_key, aes_iv

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

try:
    from pyaes import AES
except ImportError:
    pass

BLOCK_SIZE = 16


# TODO: Performance optimization

class IGE:
    @classmethod
    def encrypt(cls, data: bytes, key: bytes, iv: bytes) -> bytes:
        return cls.ige(data, key, iv, True)

    @classmethod
    def decrypt(cls, data: bytes, key: bytes, iv: bytes) -> bytes:
        return cls.ige(data, key, iv, False)

    @staticmethod
    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )

    @classmethod
    def ige(cls, data: bytes, key: bytes, iv: bytes, encrypt: bool) -> bytes:
        cipher = AES(key)

        iv_1 = iv[:BLOCK_SIZE]
        iv_2 = iv[BLOCK_SIZE:]

        data = [data[i: i + BLOCK_SIZE] for i in range(0, len(data), BLOCK_SIZE)]

        if encrypt:
            for i, chunk in enumerate(data):
                iv_1 = data[i] = cls.xor(cipher.encrypt(cls.xor(chunk, iv_1)), iv_2)
                iv_2 = chunk
        else:
            for i, chunk in enumerate(data):
                iv_2 = data[i] = cls.xor(cipher.decrypt(cls.xor(chunk, iv_2)), iv_1)
                iv_1 = chunk

        return b"".join(data)

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

import logging

log = logging.getLogger(__name__)

try:
    import tgcrypto
except ImportError:
    log.warning(
        "TgCrypto is missing! "
        "Pyrogram will work the same, but at a much slower speed. "
        "More info: https://docs.pyrogram.ml/resources/TgCrypto"
    )
    is_fast = False
    import pyaes
else:
    log.info("Using TgCrypto")
    is_fast = True


# TODO: Ugly IFs
class AES:
    @classmethod
    def ige_encrypt(cls, data: bytes, key: bytes, iv: bytes) -> bytes:
        if is_fast:
            return tgcrypto.ige_encrypt(data, key, iv)
        else:
            return cls.ige(data, key, iv, True)

    @classmethod
    def ige_decrypt(cls, data: bytes, key: bytes, iv: bytes) -> bytes:
        if is_fast:
            return tgcrypto.ige_decrypt(data, key, iv)
        else:
            return cls.ige(data, key, iv, False)

    @staticmethod
    def ctr_decrypt(data: bytes, key: bytes, iv: bytes, offset: int) -> bytes:
        replace = int.to_bytes(offset // 16, byteorder="big", length=4)
        iv = iv[:-4] + replace

        if is_fast:
            return tgcrypto.ctr_decrypt(data, key, iv)
        else:
            ctr = pyaes.AESModeOfOperationCTR(key)
            ctr._counter._counter = list(iv)
            return ctr.decrypt(data)

    @staticmethod
    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )

    @classmethod
    def ige(cls, data: bytes, key: bytes, iv: bytes, encrypt: bool) -> bytes:
        cipher = pyaes.AES(key)

        iv_1 = iv[:16]
        iv_2 = iv[16:]

        data = [data[i: i + 16] for i in range(0, len(data), 16)]

        if encrypt:
            for i, chunk in enumerate(data):
                iv_1 = data[i] = cls.xor(cipher.encrypt(cls.xor(chunk, iv_1)), iv_2)
                iv_2 = chunk
        else:
            for i, chunk in enumerate(data):
                iv_2 = data[i] = cls.xor(cipher.decrypt(cls.xor(chunk, iv_2)), iv_1)
                iv_1 = chunk

        return b"".join(data)

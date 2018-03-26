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

import sys

try:
    import tgcrypto
except ImportError:
    sys.exit(
        "TgCrypto is missing and Pyrogram can't run without. "
        "Please install it using \"pip3 install tgcrypto\". "
        "More info: https://docs.pyrogram.ml/resources/TgCrypto"
    )


# TODO: Ugly IFs
class AES:
    @classmethod
    def ige_encrypt(cls, data: bytes, key: bytes, iv: bytes) -> bytes:
        return tgcrypto.ige_encrypt(data, key, iv)

    @classmethod
    def ige_decrypt(cls, data: bytes, key: bytes, iv: bytes) -> bytes:
        return tgcrypto.ige_decrypt(data, key, iv)

    @staticmethod
    def ctr_decrypt(data: bytes, key: bytes, iv: bytes, offset: int) -> bytes:
        replace = int.to_bytes(offset // 16, 4, "big")
        iv = iv[:-4] + replace

        return tgcrypto.ctr_decrypt(data, key, iv)

    @staticmethod
    def xor(a: bytes, b: bytes) -> bytes:
        return int.to_bytes(
            int.from_bytes(a, "big") ^ int.from_bytes(b, "big"),
            len(a),
            "big",
        )

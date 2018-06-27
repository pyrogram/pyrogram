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
import os

from .tcp import TCP
from ....crypto.aes import AES

log = logging.getLogger(__name__)


class TCPAbridgedO(TCP):
    RESERVED = (b"HEAD", b"POST", b"GET ", b"OPTI", b"\xee" * 4)

    def __init__(self, proxy: dict):
        super().__init__(proxy)
        self.encrypt = None
        self.decrypt = None

    def connect(self, address: tuple):
        super().connect(address)

        while True:
            nonce = bytearray(os.urandom(64))

            if (nonce[0] != b"\xef"
                    and nonce[:4] not in self.RESERVED
                    and nonce[4:4] != b"\x00" * 4):
                nonce[56] = nonce[57] = nonce[58] = nonce[59] = 0xef
                break

        temp = bytearray(nonce[55:7:-1])

        self.encrypt = (nonce[8:40], nonce[40:56], bytearray(1))
        self.decrypt = (temp[0:32], temp[32:48], bytearray(1))

        nonce[56:64] = AES.ctr256_encrypt(nonce, *self.encrypt)[56:64]

        super().sendall(nonce)

        log.info("Connected{}!".format(" with proxy" if self.proxy_enabled else ""))

    def sendall(self, data: bytes, *args):
        length = len(data) // 4

        super().sendall(
            AES.ctr256_encrypt(
                (bytes([length])
                 if length <= 126
                 else b"\x7f" + length.to_bytes(3, "little"))
                + data,
                *self.encrypt
            )
        )

    def recvall(self, length: int = 0) -> bytes or None:
        length = super().recvall(1)

        if length is None:
            return None

        length = AES.ctr256_decrypt(length, *self.decrypt)

        if length == b"\x7f":
            length = super().recvall(3)

            if length is None:
                return None

            length = AES.ctr256_decrypt(length, *self.decrypt)

        data = super().recvall(int.from_bytes(length, "little") * 4)

        if data is None:
            return None

        return AES.ctr256_decrypt(data, *self.decrypt)

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

from .tcp import TCP

log = logging.getLogger(__name__)


class TCPAbridged(TCP):
    def __init__(self, proxy: dict):
        super().__init__(proxy)

    def connect(self, address: tuple):
        super().connect(address)
        super().sendall(b"\xef")

        log.info("Connected{}!".format(" with proxy" if self.proxy_enabled else ""))

    def sendall(self, data: bytes, *args):
        length = len(data) // 4

        super().sendall(
            (bytes([length])
             if length <= 126
             else b"\x7f" + length.to_bytes(3, "little"))
            + data
        )

    def recvall(self, length: int = 0) -> bytes or None:
        length = super().recvall(1)

        if length is None:
            return None

        if length == b"\x7f":
            length = super().recvall(3)

            if length is None:
                return None

        return super().recvall(int.from_bytes(length, "little") * 4)

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

import logging

from .tcp import TCP

log = logging.getLogger(__name__)


class TCPAbridged(TCP):
    def __init__(self):
        super().__init__()
        self.is_first_packet = None

    def connect(self, address: tuple):
        super().connect(address)
        self.is_first_packet = True
        log.info("Connected!")

    def send(self, data: bytes):
        length = len(data) // 4

        data = (
            bytes([length]) + data
            if length <= 126
            else b"\x7f" + int.to_bytes(length, 3, "little") + data
        )

        if self.is_first_packet:
            data = b"\xef" + data
            self.is_first_packet = False

        super().sendall(data)

    def recv(self) -> bytes or None:
        length = self.recvall(1)

        if length is None:
            return None

        if length == b"\x7f":
            length = self.recvall(3)

            if length is None:
                return None

        length = int.from_bytes(length, "little") * 4

        packet = self.recvall(length)

        return packet

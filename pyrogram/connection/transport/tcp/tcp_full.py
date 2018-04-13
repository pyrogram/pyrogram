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
from binascii import crc32
from struct import pack, unpack

from .tcp import TCP

log = logging.getLogger(__name__)


class TCPFull(TCP):
    def __init__(self, proxy: dict):
        super().__init__(proxy)
        self.seq_no = None

    def connect(self, address: tuple):
        super().connect(address)
        self.seq_no = 0
        log.info("Connected{}!".format(" with proxy" if self.proxy_enabled else ""))

    def sendall(self, data: bytes, *args):
        # 12 = packet_length (4), seq_no (4), crc32 (4) (at the end)
        data = pack("<II", len(data) + 12, self.seq_no) + data
        data += pack("<I", crc32(data))
        self.seq_no += 1

        super().sendall(data)

    def recvall(self, length: int = 0) -> bytes or None:
        length = super().recvall(4)

        if length is None:
            return None

        packet = super().recvall(unpack("<I", length)[0] - 4)

        if packet is None:
            return None

        packet = length + packet  # Whole data + checksum
        checksum = packet[-4:]  # Checksum is at the last 4 bytes
        packet = packet[:-4]  # Data without checksum

        if crc32(packet) != unpack("<I", checksum)[0]:
            return None

        return packet[8:]  # Skip packet_length (4) and tcp_seq_no (4)

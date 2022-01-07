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

import logging
from struct import pack, unpack
from typing import Optional

from .tcp import TCP

log = logging.getLogger(__name__)


class TCPIntermediate(TCP):
    def __init__(self, ipv6: bool, proxy: dict):
        super().__init__(ipv6, proxy)

    async def connect(self, address: tuple):
        await super().connect(address)
        await super().send(b"\xee" * 4)

    async def send(self, data: bytes, *args):
        await super().send(pack("<i", len(data)) + data)

    async def recv(self, length: int = 0) -> Optional[bytes]:
        length = await super().recv(4)

        if length is None:
            return None

        return await super().recv(unpack("<i", length)[0])

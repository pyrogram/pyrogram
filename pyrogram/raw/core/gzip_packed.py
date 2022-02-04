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

from gzip import compress, decompress
from io import BytesIO
from typing import cast, Any

from .primitives.bytes import Bytes
from .primitives.int import Int
from .tl_object import TLObject


class GzipPacked(TLObject):
    ID = 0x3072CFA1

    __slots__ = ["packed_data"]

    QUALNAME = "GzipPacked"

    def __init__(self, packed_data: TLObject):
        self.packed_data = packed_data

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "GzipPacked":
        # Return the Object itself instead of a GzipPacked wrapping it
        return cast(GzipPacked, TLObject.read(
            BytesIO(
                decompress(
                    Bytes.read(data)
                )
            )
        ))

    def write(self, *args: Any) -> bytes:
        b = BytesIO()

        b.write(Int(self.ID, False))

        b.write(
            Bytes(
                compress(
                    self.packed_data.write()
                )
            )
        )

        return b.getvalue()

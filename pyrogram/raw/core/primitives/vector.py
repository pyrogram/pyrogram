#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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

from io import BytesIO
from typing import cast, Union, Any

from .int import Int, Long
from ..list import List
from ..tl_object import TLObject


class Vector(bytes, TLObject):
    ID = 0x1CB5C415

    # Method added to handle the special case when a query returns a bare Vector (of Ints);
    # i.e., RpcResult body starts with 0x1cb5c415 (Vector Id) - e.g., messages.GetMessagesViews.
    @staticmethod
    def read_bare(b: BytesIO, n: int) -> Union[int, Any]:
        left = len(b.read())
        size = left // n
        b.seek(-left, 1)

        try:
            return TLObject.read(b)
        except KeyError:
            b.seek(-4, 1)

            if size == 4:
                return Int.read(b)
            else:
                return Long.read(b)

    @classmethod
    def read(cls, data: BytesIO, t: Any = None, *args: Any) -> List:
        count = Int.read(data)

        return List(
            t.read(data) if t
            else Vector.read_bare(data, count)
            for _ in range(count)
        )

    def __new__(cls, value: list, t: Any = None) -> bytes:  # type: ignore
        return b"".join(
            [Int(cls.ID, False), Int(len(value))]
            + [cast(bytes, t(i)) if t else i.write() for i in value]
        )

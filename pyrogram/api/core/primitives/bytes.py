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

from io import BytesIO

from ..object import Object


class Bytes(Object):
    @staticmethod
    def read(b: BytesIO, *args) -> bytes:
        length = int.from_bytes(b.read(1), "little")

        if length <= 253:
            x = b.read(length)
            b.read(-(length + 1) % 4)
        else:
            length = int.from_bytes(b.read(3), "little")
            x = b.read(length)
            b.read(-length % 4)

        return x

    def __new__(cls, value: bytes) -> bytes:
        length = len(value)

        if length <= 253:
            return (
                bytes([length])
                + value
                + bytes(-(length + 1) % 4)
            )
        else:
            return (
                bytes([254])
                + int.to_bytes(length, 3, "little")
                + value
                + bytes(-length % 4)
            )

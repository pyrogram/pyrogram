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


class Int(Object):
    SIZE = 4

    @classmethod
    def read(cls, b: BytesIO, signed: bool = True) -> int:
        return int.from_bytes(b.read(cls.SIZE), "little", signed=signed)

    def __new__(cls, value: int, signed: bool = True) -> bytes:
        return int.to_bytes(value, cls.SIZE, "little", signed=signed)


class Long(Int):
    SIZE = 8

    def __new__(cls, *args):
        return super().__new__(cls, *args)


class Int128(Int):
    SIZE = 16


class Int256(Int):
    SIZE = 32

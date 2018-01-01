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

from datetime import datetime
from io import BytesIO

from .object import Object
from .primitives import Int, Long


class FutureSalt(Object):
    ID = 0x0949d9dc

    def __init__(self, valid_since: int or datetime, valid_until: int or datetime, salt: int):
        self.valid_since = valid_since
        self.valid_until = valid_until
        self.salt = salt

    @staticmethod
    def read(b: BytesIO, *args) -> "FutureSalt":
        valid_since = datetime.fromtimestamp(Int.read(b))
        valid_until = datetime.fromtimestamp(Int.read(b))
        salt = Long.read(b)

        return FutureSalt(valid_since, valid_until, salt)

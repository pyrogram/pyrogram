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

from . import FutureSalt
from .object import Object
from .primitives import Int, Long


class FutureSalts(Object):
    ID = 0xae500895

    def __init__(self, req_msg_id: int, now: int or datetime, salts: list):
        self.req_msg_id = req_msg_id
        self.now = now
        self.salts = salts

    @staticmethod
    def read(b: BytesIO, *args) -> "FutureSalts":
        req_msg_id = Long.read(b)
        now = datetime.fromtimestamp(Int.read(b))

        count = Int.read(b)
        salts = [FutureSalt.read(b) for _ in range(count)]

        return FutureSalts(req_msg_id, now, salts)

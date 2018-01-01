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

from .object import Object
from .primitives import Int, Long


class Message(Object):
    ID = 0x5bb8e511  # hex(crc32(b"message msg_id:long seqno:int bytes:int body:Object = Message"))

    def __init__(self, body: Object, msg_id: int, seq_no: int, length: int):
        self.msg_id = msg_id
        self.seq_no = seq_no
        self.length = length
        self.body = body

    @staticmethod
    def read(b: BytesIO, *args) -> "Message":
        msg_id = Long.read(b)
        seq_no = Int.read(b)
        length = Int.read(b)
        body = b.read(length)

        return Message(Object.read(BytesIO(body)), msg_id, seq_no, length)

    def write(self) -> bytes:
        b = BytesIO()

        b.write(Long(self.msg_id))
        b.write(Int(self.seq_no))
        b.write(Int(self.length))
        b.write(self.body.write())

        return b.getvalue()

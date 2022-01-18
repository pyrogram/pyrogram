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

from io import BytesIO
from typing import List, Any

from .message import Message
from .primitives.int import Int
from .tl_object import TLObject


class MsgContainer(TLObject):
    ID = 0x73F1F8DC

    __slots__ = ["messages"]

    QUALNAME = "MsgContainer"

    def __init__(self, messages: List[Message]):
        self.messages = messages

    @staticmethod
    def read(data: BytesIO, *args: Any) -> "MsgContainer":
        count = Int.read(data)
        return MsgContainer([Message.read(data) for _ in range(count)])

    def write(self, *args: Any) -> bytes:
        b = BytesIO()

        b.write(Int(self.ID, False))

        count = len(self.messages)
        b.write(Int(count))

        for message in self.messages:
            b.write(message.write())

        return b.getvalue()

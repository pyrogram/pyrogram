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

from pyrogram.api import types
from .message import Message
from ..pyrogram_type import PyrogramType


class Messages(PyrogramType):
    """This object represents a chat's messages.

    Args:
        total_count (``int``):
            Total number of messages the target chat has.

        messages (List of :obj:`Message <pyrogram.Message>`):
            Requested messages.
    """

    def __init__(self, *, client, raw, total_count: int, messages: list):
        super().__init__(client, raw)

        self.total_count = total_count
        self.messages = messages

    @staticmethod
    def parse(client, messages: types.messages.Messages) -> "Messages":
        users = {i.id: i for i in messages.users}
        chats = {i.id: i for i in messages.chats}

        return Messages(
            total_count=getattr(messages, "count", len(messages.messages)),
            messages=[Message.parse(client, message, users, chats) for message in messages.messages],
            client=client,
            raw=messages
        )

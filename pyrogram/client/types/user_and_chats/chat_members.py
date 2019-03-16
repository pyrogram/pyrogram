# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

from typing import List

import pyrogram
from pyrogram.api import types
from .chat_member import ChatMember
from ..pyrogram_type import PyrogramType


class ChatMembers(PyrogramType):
    """This object contains information about the members list of a chat.

    Args:
        total_count (``int``):
            Total number of members the chat has.

        chat_members (List of :obj:`ChatMember <pyrogram.ChatMember>`):
            Requested chat members.
    """

    __slots__ = ["total_count", "chat_members"]

    def __init__(
            self,
            *,
            client: "pyrogram.client.ext.BaseClient",
            total_count: int,
            chat_members: List[ChatMember]
    ):
        super().__init__(client)

        self.total_count = total_count
        self.chat_members = chat_members

    @staticmethod
    def _parse(client, members):
        users = {i.id: i for i in members.users}
        chat_members = []

        if isinstance(members, types.channels.ChannelParticipants):
            total_count = members.count
            members = members.participants
        else:
            members = members.full_chat.participants.participants
            total_count = len(members)

        for member in members:
            chat_members.append(ChatMember._parse(client, member, users))

        return ChatMembers(
            total_count=total_count,
            chat_members=chat_members,
            client=client
        )

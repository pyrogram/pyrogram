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
from ..pyrogram_type import PyrogramType
from ..user_and_chats import ChatMember, User


class ChatMembers(PyrogramType):
    """This object contains information about the members list of a chat.

    Args:
        total_count (``int``):
            Total number of members the chat has.

        chat_members (List of :obj:`ChatMember <pyrogram.ChatMember>`):
            Requested chat members.
    """

    def __init__(self, *, total_count: int, chat_members: list, client=None):
        self.total_count = total_count
        self.chat_members = chat_members

        self.client = client

    @staticmethod
    def parse(client, members, users: dict):
        if isinstance(members, types.channels.ChannelParticipants):
            total_count = members.count
            members = members.participants
        else:
            members = members.full_chat.participants.participants
            total_count = len(members)

        chat_members = []

        for member in members:
            user = User.parse(client, users[member.user_id])
            chat_members.append(ChatMember.parse(client, member, user))

        return ChatMembers(
            total_count=total_count,
            chat_members=chat_members,
            client=client
        )

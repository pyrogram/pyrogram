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

from typing import List, Dict

from pyrogram import raw, types
from ..object import Object


class VoiceChatMembersInvited(Object):
    """A service message about new members invited to a voice chat.


    Parameters:
        users (List of :obj:`~pyrogram.types.User`):
            New members that were invited to the voice chat.
    """

    def __init__(
        self, *,
        users: List["types.User"]
    ):
        super().__init__()

        self.users = users

    @staticmethod
    def _parse(
        client,
        action: "raw.types.MessageActionInviteToGroupCall",
        users: Dict[int, "raw.types.User"]
    ) -> "VoiceChatMembersInvited":
        users = [types.User._parse(client, users[i]) for i in action.users]

        return VoiceChatMembersInvited(users=users)

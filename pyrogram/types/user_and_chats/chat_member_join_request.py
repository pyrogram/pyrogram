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

from typing import Dict, Union

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object
from ..update import Update


class ChatMemberJoinRequest(Object, Update):
    """New user join request in a private chat.

    Parameters:
        chat (:obj:`~pyrogram.types.Chat`):
            Chat the user belongs to.

        requester (:obj:`~pyrogram.types.User`):
            Performer of the action, which resulted in the change.

        invite_link (:obj:`~pyrogram.types.ChatInviteLink`, *optional*):
            Chat invite link, which was used by the user to join the chat; for joining by invite link events only.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        chat: "types.Chat",
        requester: "types.User",
        invite_link: "types.ChatInviteLink" = None,
    ):
        super().__init__(client)

        self.chat = chat
        self.requester = requester
        self.invite_link = invite_link

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        update: Union["raw.types.UpdateChatParticipant", "raw.types.UpdateChannelParticipant"],
        users: Dict[int, "raw.types.User"],
        chats: Dict[int, "raw.types.Chat"]
    ) -> "ChatMemberJoinRequest":
        invite_link = None

        if update.invite:
            invite_link = types.ChatInviteLink._parse(client, update.invite, users)

        return ChatMemberJoinRequest(
            chat=types.Chat._parse_chat(client, next(iter(chats.values()))),
            requester=types.User._parse(client, users[update.user_id]),
            invite_link=invite_link,
            client=client
        )

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

from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class ChatPreview(Object):
    """A chat preview.

    Parameters:
        title (``str``):
            Title of the chat.

        type (``str``):
            Type of chat, can be either, "group", "supergroup" or "channel".

        members_count (``int``):
            Chat members count.

        photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Chat photo.

        members (List of :obj:`~pyrogram.types.User`, *optional*):
            Preview of some of the chat members.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        title: str,
        type: str,
        members_count: int,
        photo: "types.Photo" = None,
        members: List["types.User"] = None
    ):
        super().__init__(client)

        self.title = title
        self.type = type
        self.members_count = members_count
        self.photo = photo
        self.members = members

    @staticmethod
    def _parse(client, chat_invite: "raw.types.ChatInvite") -> "ChatPreview":
        return ChatPreview(
            title=chat_invite.title,
            type=("group" if not chat_invite.channel else
                  "channel" if chat_invite.broadcast else
                  "supergroup"),
            members_count=chat_invite.participants_count,
            photo=types.Photo._parse(client, chat_invite.photo),
            members=[types.User._parse(client, user) for user in chat_invite.participants] or None,
            client=client
        )

    # TODO: Maybe just merge this object into Chat itself by adding the "members" field.
    #  get_chat can be used as well instead of get_chat_preview

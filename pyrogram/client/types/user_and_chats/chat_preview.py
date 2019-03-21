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
from .chat_photo import ChatPhoto
from ..pyrogram_type import PyrogramType
from ..user_and_chats.user import User


class ChatPreview(PyrogramType):
    """This object represents a chat preview.

    Args:
        title (``str``):
            Title of the chat.

        photo (:obj:`ChatPhoto`):
            Chat photo. Suitable for downloads only.

        type (``str``):
            Type of chat, can be either, "group", "supergroup" or "channel".

        members_count (``int``):
            Chat members count.

        members (List of :obj:`User`, *optional*):
            Preview of some of the chat members.
    """

    __slots__ = ["title", "photo", "type", "members_count", "members"]

    def __init__(
        self,
        *,
        client: "pyrogram.client.ext.BaseClient",
        title: str,
        photo: ChatPhoto,
        type: str,
        members_count: int,
        members: List[User] = None
    ):
        super().__init__(client)

        self.title = title
        self.photo = photo
        self.type = type
        self.members_count = members_count
        self.members = members

    @staticmethod
    def _parse(client, chat_invite: types.ChatInvite) -> "ChatPreview":
        return ChatPreview(
            title=chat_invite.title,
            photo=ChatPhoto._parse(client, chat_invite.photo),
            type=("group" if not chat_invite.channel else
                  "channel" if chat_invite.broadcast else
                  "supergroup"),
            members_count=chat_invite.participants_count,
            members=[User._parse(client, user) for user in chat_invite.participants] or None,
            client=client
        )

    # TODO: Maybe just merge this object into Chat itself by adding the "members" field.
    #  get_chat can be used as well instead of get_chat_preview

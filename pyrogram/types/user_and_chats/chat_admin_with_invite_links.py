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

from typing import Dict

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class ChatAdminWithInviteLinks(Object):
    """Represents a chat administrator that has created invite links in a chat.

    Parameters:
        admin (:obj:`~pyrogram.types.User`):
            The administrator.

        chat_invite_links_count (``int``):
            The number of valid chat invite links created by this administrator.

        revoked_chat_invite_links_count (``int``):
            The number of revoked chat invite links created by this administrator.
    """

    def __init__(
        self, *,
        admin: "types.User",
        chat_invite_links_count: int,
        revoked_chat_invite_links_count: int = None
    ):
        super().__init__()

        self.admin = admin
        self.chat_invite_links_count = chat_invite_links_count
        self.revoked_chat_invite_links_count = revoked_chat_invite_links_count

    @staticmethod
    def _parse(
        client: "pyrogram.Client",
        admin: "raw.types.ChatAdminWithInvites",
        users: Dict[int, "raw.types.User"] = None
    ) -> "ChatAdminWithInviteLinks":
        return ChatAdminWithInviteLinks(
            admin=types.User._parse(client, users[admin.admin_id]),
            chat_invite_links_count=admin.invites_count,
            revoked_chat_invite_links_count=admin.revoked_invites_count
        )

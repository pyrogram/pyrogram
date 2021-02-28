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
from typing import Union

from pyrogram import raw
from ..object import Object


class InviteLink(Object):
    """An invite link.

    Parameters:
        link (``str``):
            The invite link in full.

        date (``int``):
            The unix time when the link was exported

        revoked (``bool``):
            Whether or not the invite link has been revoked. Once a link is revoked, it cannot be restored.

        permanent (``bool``):
            Whether or not the invite link is the primary link which needs to be manually revoked.

        expire_date (``int``):
            Unix time when the invite link will expire.
            Expired links can be extended with ``edit_exported_chat_invite``

        usage_limit (``int``):
            How many users can join with this link.
    """

    def __init__(
        self, *, link: str, date: int, revoked: bool, permanent: bool, expire_date: int, usage_limit: int
    ):
        super().__init__(None)

        self.link = link
        self.date = date
        self.revoked = revoked
        self.permanent = permanent
        self.expire_date = expire_date
        self.usage_limit = usage_limit

    @staticmethod
    def _parse(invite: Union["raw.types.ChatInviteExported", "raw.types.messages.ExportedChatInvite"]) -> "InviteLink":
        # EditExportedChatInvite returns a slightly different type to ExportChatInviteLink, hence this "hack"
        if isinstance(invite, raw.types.messages.ExportedChatInvite):
            invite = invite.invite

        return InviteLink(
            link=invite.link,
            date=invite.date,
            revoked=invite.revoked,
            permanent=invite.permanent,
            expire_date=invite.expire_date,
            usage_limit=invite.usage_limit
        )

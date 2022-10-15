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

from typing import Union

import pyrogram
from pyrogram import raw


class DeleteChatAdminInviteLinks:
    async def delete_chat_admin_invite_links(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        admin_id: Union[int, str],
    ) -> bool:
        """Delete all revoked invite links of an administrator.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

            admin_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For you yourself you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            ``bool``: On success ``True`` is returned.
        """

        return await self.invoke(
            raw.functions.messages.DeleteRevokedExportedChatInvites(
                peer=await self.resolve_peer(chat_id),
                admin_id=await self.resolve_peer(admin_id),
            )
        )

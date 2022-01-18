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

from pyrogram import raw
from pyrogram.scaffold import Scaffold


class GetChatAdminInviteLinksCount(Scaffold):
    async def get_chat_admin_invite_links_count(
        self,
        chat_id: Union[int, str],
        admin_id: Union[int, str],
        revoked: bool = False,
    ) -> int:
        """Get the count of the invite links created by an administrator in a chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

            admin_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For you yourself you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            revoked (``bool``, *optional*):
                True, if you want to get revoked links instead.
                Defaults to False (get active links only).

        Returns:
            ``int``: On success, the invite links count is returned.
        """
        r = await self.send(
            raw.functions.messages.GetExportedChatInvites(
                peer=await self.resolve_peer(chat_id),
                admin_id=await self.resolve_peer(admin_id),
                limit=1,
                revoked=revoked
            )
        )

        return r.count

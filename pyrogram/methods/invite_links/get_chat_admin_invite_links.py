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

from typing import Union, Optional, AsyncGenerator

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class GetChatAdminInviteLinks(Scaffold):
    async def get_chat_admin_invite_links(
        self,
        chat_id: Union[int, str],
        admin_id: Union[int, str],
        revoked: bool = False,
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.ChatInviteLink", None]]:
        """Get the invite links created by an administrator in a chat.

        .. note::

            As an administrator you can only get your own links you have exported.
            As the chat or channel owner you can get everyones links.

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

            limit (``int``, *optional*):
                Limits the number of invite links to be retrieved.
                By default, no limit is applied and all invite links are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.ChatInviteLink` objects.

        Yields:
            :obj:`~pyrogram.types.ChatInviteLink` objects.
        """
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        offset_date = None
        offset_link = None

        while True:
            r = await self.send(
                raw.functions.messages.GetExportedChatInvites(
                    peer=await self.resolve_peer(chat_id),
                    admin_id=await self.resolve_peer(admin_id),
                    limit=limit,
                    revoked=revoked,
                    offset_date=offset_date,
                    offset_link=offset_link
                )
            )

            if not r.invites:
                break

            users = {i.id: i for i in r.users}

            offset_date = r.invites[-1].date
            offset_link = r.invites[-1].link

            for i in r.invites:
                yield types.ChatInviteLink._parse(self, i, users)

                current += 1

                if current >= total:
                    return

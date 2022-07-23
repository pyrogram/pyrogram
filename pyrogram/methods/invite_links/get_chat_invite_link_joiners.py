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

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetChatInviteLinkJoiners:
    async def get_chat_invite_link_joiners(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        invite_link: str,
        limit: int = 0
    ) -> Optional[AsyncGenerator["types.ChatJoiner", None]]:
        """Get the members who joined the chat with the invite link.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

            invite_link (str):
                The invite link.

            limit (``int``, *optional*):
                Limits the number of invite links to be retrieved.
                By default, no limit is applied and all invite links are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.ChatJoiner` objects.

        Yields:
            :obj:`~pyrogram.types.ChatJoiner` objects.
        """
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        offset_date = 0
        offset_user = raw.types.InputUserEmpty()

        while True:
            r = await self.invoke(
                raw.functions.messages.GetChatInviteImporters(
                    peer=await self.resolve_peer(chat_id),
                    link=invite_link,
                    limit=limit,
                    offset_date=offset_date,
                    offset_user=offset_user
                )
            )

            if not r.importers:
                break

            users = {i.id: i for i in r.users}

            offset_date = r.importers[-1].date
            offset_user = await self.resolve_peer(r.importers[-1].user_id)

            for i in r.importers:
                yield types.ChatJoiner._parse(self, i, users)

                current += 1

                if current >= total:
                    return

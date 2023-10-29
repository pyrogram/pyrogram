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
from pyrogram import types


class ApplyBoost:
    async def apply_boost(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
    ) -> bool:
        """Apply boost

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            :obj:`~pyrogram.types.MyBoost`: On success, a boost object is returned.

        Example:
            .. code-block:: python

                # Apply boost to chat id
                app.apply_boost(chat_id)
        """
        r = await self.invoke(
            raw.functions.premium.ApplyBoost(
                peer=await self.resolve_peer(chat_id),
            )
        )

        return types.MyBoost._parse(
            self,
            r.my_boosts[0],
            {i.id: i for i in r.users},
            {i.id: i for i in r.chats}
        )

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

from typing import Union, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types


class CanSendStory:
    async def can_send_story(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
    ) -> bool:
        """Can send story

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            ``str``: On success, a bool is returned.

        Example:
            .. code-block:: python

                # Check if you can send story to chat id
                app.can_send_story(chat_id)
        """
        r = await self.invoke(
            raw.functions.stories.CanSendStory(
                peer=await self.resolve_peer(chat_id),
            )
        )

        return r

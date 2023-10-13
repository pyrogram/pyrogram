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

from typing import List, Union

import pyrogram
from pyrogram import raw, types


class ReadStories:
    async def read_stories(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        max_id: int = 0,
    ) -> List[int]:
        """Read stories.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            max_id (``int``, *optional*):
                Maximum identifier of the target story to read.

        Returns:
            List of ``int``: On success, a list of read stories is returned.

        Example:
            .. code-block:: python

                # Read stories
                await app.read_stories(chat_id)
        """
        r = await self.invoke(
            raw.functions.stories.ReadStories(
                peer=await self.resolve_peer(chat_id),
                max_id=max_id
            )
        )

        return types.List(r)

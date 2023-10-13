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

from typing import List, Union, Iterable

import pyrogram
from pyrogram import raw
from pyrogram import types


class DeleteStories:
    async def delete_stories(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        story_ids: Union[int, Iterable[int]],
    ) -> List[int]:
        """Delete stories.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            story_ids (``int`` | ``list``):
                Unique identifier (int) or list of unique identifiers (list of int) for the target stories.

        Returns:
            List of ``int``: List of deleted stories IDs

        Example:
            .. code-block:: python

                # Delete a single story
                app.delete_stories(chat_id, 1)

                # Delete multiple stories
                app.delete_stories(chat_id, [1, 2])
        """
        is_iterable = not isinstance(story_ids, int)
        ids = list(story_ids) if is_iterable else [story_ids]

        r = await self.invoke(
            raw.functions.stories.DeleteStories(
                peer=await self.resolve_peer(chat_id),
                id=ids
            )
        )

        return types.List(r)

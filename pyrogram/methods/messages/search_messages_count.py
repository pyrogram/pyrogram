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
from pyrogram import raw, enums


class SearchMessagesCount:
    async def search_messages_count(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        query: str = "",
        filter: "enums.MessagesFilter" = enums.MessagesFilter.EMPTY,
        from_user: Union[int, str] = None
    ) -> int:
        """Get the count of messages resulting from a search inside a chat.

        If you want to get the actual messages, see :meth:`~pyrogram.Client.search_messages`.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            query (``str``, *optional*):
                Text query string.
                Required for text-only messages, optional for media messages (see the ``filter`` argument).
                When passed while searching for media messages, the query will be applied to captions.
                Defaults to "" (empty string).

            filter (:obj:`~pyrogram.enums.MessagesFilter`, *optional*):
                Pass a filter in order to search for specific kind of messages only:

            from_user (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target user you want to search for messages from.

        Returns:
            ``int``: On success, the messages count is returned.
        """
        r = await self.invoke(
            raw.functions.messages.Search(
                peer=await self.resolve_peer(chat_id),
                q=query,
                filter=filter.value(),
                min_date=0,
                max_date=0,
                offset_id=0,
                add_offset=0,
                limit=1,
                min_id=0,
                max_id=0,
                from_id=(
                    await self.resolve_peer(from_user)
                    if from_user
                    else None
                ),
                hash=0
            )
        )

        if hasattr(r, "count"):
            return r.count
        else:
            return len(r.messages)

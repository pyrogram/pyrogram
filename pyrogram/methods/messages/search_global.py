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

from typing import AsyncGenerator, Optional

import pyrogram
from pyrogram import raw, enums
from pyrogram import types
from pyrogram import utils


class SearchGlobal:
    async def search_global(
        self: "pyrogram.Client",
        query: str = "",
        filter: "enums.MessagesFilter" = enums.MessagesFilter.EMPTY,
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Search messages globally from all of your chats.

        If you want to get the messages count only, see :meth:`~pyrogram.Client.search_global_count`.

        .. note::

            Due to server-side limitations, you can only get up to around ~10,000 messages and each message
            retrieved will not have any *reply_to_message* field.

        Parameters:
            query (``str``, *optional*):
                Text query string.
                Use "@" to search for mentions.
            
            filter (:obj:`~pyrogram.enums.MessagesFilter`, *optional*):
                Pass a filter in order to search for specific kind of messages only.
                Defaults to any message (no filter).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.

        Example:
            .. code-block:: python

                from pyrogram import enums

                # Search for "pyrogram". Get the first 50 results
                async for message in app.search_global("pyrogram", limit=50):
                    print(message.text)

                # Search for recent photos from Global. Get the first 20 results
                async for message in app.search_global(filter=enums.MessagesFilter.PHOTO, limit=20):
                    print(message.photo)
        """
        current = 0
        # There seems to be an hard limit of 10k, beyond which Telegram starts spitting one message at a time.
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        offset_date = 0
        offset_peer = raw.types.InputPeerEmpty()
        offset_id = 0

        while True:
            messages = await utils.parse_messages(
                self,
                await self.invoke(
                    raw.functions.messages.SearchGlobal(
                        q=query,
                        filter=filter.value(),
                        min_date=0,
                        max_date=0,
                        offset_rate=offset_date,
                        offset_peer=offset_peer,
                        offset_id=offset_id,
                        limit=limit
                    ),
                    sleep_threshold=60
                ),
                replies=0
            )

            if not messages:
                return

            last = messages[-1]

            offset_date = last.date
            offset_peer = await self.resolve_peer(last.chat.id)
            offset_id = last.id

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return

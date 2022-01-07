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

from typing import Union, List, AsyncGenerator, Optional

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class GetChatEventLog(Scaffold):
    async def get_chat_event_log(
        self,
        chat_id: Union[int, str],
        query: str = "",
        offset_id: int = 0,
        limit: int = 0,
        filters: "types.ChatEventFilter" = None,
        user_ids: List[Union[int, str]] = None
    ) -> Optional[AsyncGenerator["types.ChatEvent", None]]:
        """Get the actions taken by chat members and administrators in the last 48h.

        Only available for supergroups and channels. Requires administrator rights.
        Results are returned in reverse chronological order (i.e., newest first).

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            query (``str``, *optional*):
                Search query to filter events based on text.
                By default, an empty query is applied and all events will be returned.

            offset_id (``int``, *optional*):
                Offset event identifier from which to start returning results.
                By default, no offset is applied and events will be returned starting from the latest.

            limit (``int``, *optional*):
                Maximum amount of events to be returned.
                By default, all events will be returned.

            filters (:obj:`~pyrogram.types.ChatEventFilter`, *optional*):
                The types of events to return.
                By default, all types will be returned.

            user_ids (List of ``int`` | ``str``, *optional*):
                User identifiers (int) or usernames (str) by which to filter events.
                By default, events relating to all users will be returned.

        Yields:
            :obj:`~pyrogram.types.ChatEvent` objects.
        """
        current = 0
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        while True:
            r: raw.base.channels.AdminLogResults = await self.send(
                raw.functions.channels.GetAdminLog(
                    channel=await self.resolve_peer(chat_id),
                    q=query,
                    min_id=0,
                    max_id=offset_id,
                    limit=limit,
                    events_filter=filters.write() if filters else None,
                    admins=(
                        [await self.resolve_peer(i) for i in user_ids]
                        if user_ids is not None
                        else user_ids
                    )
                )
            )

            if not r.events:
                return

            last = r.events[-1]
            offset_id = last.id

            for event in r.events:
                yield await types.ChatEvent._parse(self, event, r.users, r.chats)

                current += 1

                if current >= total:
                    return

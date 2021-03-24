#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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

from string import ascii_lowercase
from typing import Union, AsyncGenerator, Optional

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class Filters:
    ALL = "all"
    KICKED = "kicked"
    RESTRICTED = "restricted"
    BOTS = "bots"
    RECENT = "recent"
    ADMINISTRATORS = "administrators"


QUERIES = [""] + [str(i) for i in range(10)] + list(ascii_lowercase)
QUERYABLE_FILTERS = (Filters.ALL, Filters.KICKED, Filters.RESTRICTED)


class IterChatMembers(Scaffold):
    async def iter_chat_members(
        self,
        chat_id: Union[int, str],
        limit: int = 0,
        query: str = "",
        filter: str = Filters.RECENT
    ) -> Optional[AsyncGenerator["types.ChatMember", None]]:
        """Iterate through the members of a chat sequentially.

        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_chat_members` in a loop,
        thus saving you from the hassle of setting up boilerplate code. It is useful for getting the whole members list
        of a chat with a single call.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            limit (``int``, *optional*):
                Limits the number of members to be retrieved.
                By default, no limit is applied and all members are returned [1]_.

            query (``str``, *optional*):
                Query string to filter members based on their display names and usernames.
                Defaults to "" (empty string) [2]_.

            filter (``str``, *optional*):
                Filter used to select the kind of members you want to retrieve. Only applicable for supergroups
                and channels. It can be any of the followings:
                *"all"* - all kind of members,
                *"kicked"* - kicked (banned) members only,
                *"restricted"* - restricted members only,
                *"bots"* - bots only,
                *"recent"* - recent members only,
                *"administrators"* - chat administrators only.
                Defaults to *"recent"*.

        .. [1] Server limit: on supergroups, you can get up to 10,000 members for a single query and up to 200 members
            on channels.

        .. [2] A query string is applicable only for *"all"*, *"kicked"* and *"restricted"* filters only.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.ChatMember` objects.

        Example:
            .. code-block:: python

                # Iterate though all chat members
                for member in app.iter_chat_members("pyrogramchat"):
                    print(member.user.first_name)

                # Iterate though all administrators
                for member in app.iter_chat_members("pyrogramchat", filter="administrators"):
                    print(member.user.first_name)

                # Iterate though all bots
                for member in app.iter_chat_members("pyrogramchat", filter="bots"):
                    print(member.user.first_name)
        """
        current = 0
        yielded = set()
        queries = [query] if query else QUERIES
        total = limit or (1 << 31) - 1
        limit = min(200, total)
        resolved_chat_id = await self.resolve_peer(chat_id)

        if filter not in QUERYABLE_FILTERS:
            queries = [""]

        for q in queries:
            offset = 0

            while True:
                chat_members = await self.get_chat_members(
                    chat_id=chat_id,
                    offset=offset,
                    limit=limit,
                    query=q,
                    filter=filter
                )

                if not chat_members:
                    break

                if isinstance(resolved_chat_id, raw.types.InputPeerChat):
                    total = len(chat_members)

                offset += len(chat_members)

                for chat_member in chat_members:
                    user_id = chat_member.user.id

                    if user_id in yielded:
                        continue

                    yield chat_member

                    yielded.add(chat_member.user.id)

                    current += 1

                    if current >= total:
                        return

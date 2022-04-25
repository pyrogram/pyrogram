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

import logging
from typing import Union, Optional, AsyncGenerator

import pyrogram
from pyrogram import raw, types, enums

log = logging.getLogger(__name__)


async def get_chunk(
    client: "pyrogram.Client",
    chat_id: Union[int, str],
    offset: int,
    filter: "enums.ChatMembersFilter",
    limit: int,
    query: str,
):
    is_queryable = filter in [enums.ChatMembersFilter.SEARCH,
                              enums.ChatMembersFilter.BANNED,
                              enums.ChatMembersFilter.RESTRICTED]

    filter = filter.value(q=query) if is_queryable else filter.value()

    r = await client.invoke(
        raw.functions.channels.GetParticipants(
            channel=await client.resolve_peer(chat_id),
            filter=filter,
            offset=offset,
            limit=limit,
            hash=0
        ),
        sleep_threshold=60
    )

    members = r.participants
    users = {u.id: u for u in r.users}
    chats = {c.id: c for c in r.chats}

    return [types.ChatMember._parse(client, member, users, chats) for member in members]


class GetChatMembers:
    async def get_chat_members(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        query: str = "",
        limit: int = 0,
        filter: "enums.ChatMembersFilter" = enums.ChatMembersFilter.SEARCH
    ) -> Optional[AsyncGenerator["types.ChatMember", None]]:
        """Get the members list of a chat.

        A chat can be either a basic group, a supergroup or a channel.
        Requires administrator rights in channels.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            query (``str``, *optional*):
                Query string to filter members based on their display names and usernames.
                Only applicable to supergroups and channels. Defaults to "" (empty string).
                A query string is applicable only for :obj:`~pyrogram.enums.ChatMembersFilter.SEARCH`,
                :obj:`~pyrogram.enums.ChatMembersFilter.BANNED` and :obj:`~pyrogram.enums.ChatMembersFilter.RESTRICTED`
                filters only.

            limit (``int``, *optional*):
                Limits the number of members to be retrieved.

            filter (:obj:`~pyrogram.enums.ChatMembersFilter`, *optional*):
                Filter used to select the kind of members you want to retrieve. Only applicable for supergroups
                and channels.

        Returns:
            ``Generator``: On success, a generator yielding :obj:`~pyrogram.types.ChatMember` objects is returned.

        Example:
            .. code-block:: python

                from pyrogram import enums

                # Get members
                async for member in app.get_chat_members(chat_id):
                    print(member)

                # Get administrators
                administrators = []
                async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
                    administrators.append(m)

                # Get bots
                bots = []
                async for m in app.get_chat_members(chat_id, filter=enums.ChatMembersFilter.BOTS):
                    bots.append(m)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            r = await self.invoke(
                raw.functions.messages.GetFullChat(
                    chat_id=peer.chat_id
                )
            )

            members = getattr(r.full_chat.participants, "participants", [])
            users = {i.id: i for i in r.users}

            for member in members:
                yield types.ChatMember._parse(self, member, users, {})

            return

        current = 0
        offset = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(200, total)

        while True:
            members = await get_chunk(
                client=self,
                chat_id=chat_id,
                offset=offset,
                filter=filter,
                limit=limit,
                query=query
            )

            if not members:
                return

            offset += len(members)

            for member in members:
                yield member

                current += 1

                if current >= total:
                    return

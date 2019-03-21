# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import List

import pyrogram
from pyrogram.api import types
from ..bots.inline_query_result import InlineQueryResult
from ..messages_and_media import Location
from ..pyrogram_type import PyrogramType
from ..user_and_chats import User


class InlineQuery(PyrogramType):
    """This object represents an incoming inline query.
    When the user sends an empty query, your bot could return some default or trending results

    Args:
        id (``str``):
            Unique identifier for this query.

        from_user (:obj:`User <pyrogram.User>`):
            Sender.

        query (``str``):
            Text of the query (up to 512 characters).

        offset (``str``):
            Offset of the results to be returned, can be controlled by the bot.

        location (:obj:`Location <pyrogram.Location>`. *optional*):
            Sender location, only for bots that request user location.
    """
    __slots__ = ["id", "from_user", "query", "offset", "location"]

    def __init__(
        self,
        client: "pyrogram.client.ext.BaseClient",
        id: str,
        from_user: User,
        query: str,
        offset: str,
        location: Location = None
    ):
        super().__init__(client)

        self._client = client
        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = offset
        self.location = location

    @staticmethod
    def _parse(client, inline_query: types.UpdateBotInlineQuery, users: dict) -> "InlineQuery":
        return InlineQuery(
            client=client,
            id=str(inline_query.query_id),
            from_user=User._parse(client, users[inline_query.user_id]),
            query=inline_query.query,
            offset=inline_query.offset,
            location=Location(
                longitude=inline_query.geo.long,
                latitude=inline_query.geo.lat,
                client=client
            ) if inline_query.geo else None
        )

    def answer(
        self,
        results: List[InlineQueryResult],
        cache_time: int = 300,
        is_personal: bool = None,
        next_offset: str = "",
        switch_pm_text: str = "",
        switch_pm_parameter: str = ""
    ):
        return self._client.answer_inline_query(
            inline_query_id=self.id,
            results=results,
            cache_time=cache_time,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter
        )

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

from typing import List, Match

import pyrogram
from pyrogram import raw
from pyrogram import types, enums
from ..object import Object
from ..update import Update


class InlineQuery(Object, Update):
    """An incoming inline query.

    When the user sends an empty query, your bot could return some default or trending results.

    Parameters:
        id (``str``):
            Unique identifier for this query.

        from_user (:obj:`~pyrogram.types.User`):
            Sender.

        query (``str``):
            Text of the query (up to 512 characters).

        offset (``str``):
            Offset of the results to be returned, can be controlled by the bot.

        chat_type (:obj:`~pyrogram.enums.ChatType`, *optional*):
            Type of the chat, from which the inline query was sent.

        location (:obj:`~pyrogram.types.Location`. *optional*):
            Sender location, only for bots that request user location.

        matches (List of regex Matches, *optional*):
            A list containing all `Match Objects <https://docs.python.org/3/library/re.html#match-objects>`_ that match
            the query of this inline query. Only applicable when using :obj:`Filters.regex <pyrogram.Filters.regex>`.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        id: str,
        from_user: "types.User",
        query: str,
        offset: str,
        chat_type: "enums.ChatType",
        location: "types.Location" = None,
        matches: List[Match] = None
    ):
        super().__init__(client)

        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = offset
        self.chat_type = chat_type
        self.location = location
        self.matches = matches

    @staticmethod
    def _parse(client, inline_query: raw.types.UpdateBotInlineQuery, users: dict) -> "InlineQuery":
        peer_type = inline_query.peer_type
        chat_type = None

        if isinstance(peer_type, raw.types.InlineQueryPeerTypeSameBotPM):
            chat_type = enums.ChatType.BOT
        elif isinstance(peer_type, raw.types.InlineQueryPeerTypePM):
            chat_type = enums.ChatType.PRIVATE
        elif isinstance(peer_type, raw.types.InlineQueryPeerTypeChat):
            chat_type = enums.ChatType.GROUP
        elif isinstance(peer_type, raw.types.InlineQueryPeerTypeMegagroup):
            chat_type = enums.ChatType.SUPERGROUP
        elif isinstance(peer_type, raw.types.InlineQueryPeerTypeBroadcast):
            chat_type = enums.ChatType.CHANNEL

        return InlineQuery(
            id=str(inline_query.query_id),
            from_user=types.User._parse(client, users[inline_query.user_id]),
            query=inline_query.query,
            offset=inline_query.offset,
            chat_type=chat_type,
            location=types.Location(
                longitude=inline_query.geo.long,
                latitude=inline_query.geo.lat,
                client=client
            ) if inline_query.geo else None,
            client=client
        )

    async def answer(
        self,
        results: List["types.InlineQueryResult"],
        cache_time: int = 300,
        is_gallery: bool = False,
        is_personal: bool = False,
        next_offset: str = "",
        switch_pm_text: str = "",
        switch_pm_parameter: str = ""
    ):
        """Bound method *answer* of :obj:`~pyrogram.types.InlineQuery`.

        Use this method as a shortcut for:

        .. code-block:: python

            await client.answer_inline_query(
                inline_query.id,
                results=[...]
            )

        Example:
            .. code-block:: python

                await inline_query.answer([...])

        Parameters:
            results (List of :obj:`~pyrogram.types.InlineQueryResult`):
                A list of results for the inline query.

            cache_time (``int``, *optional*):
                The maximum amount of time in seconds that the result of the inline query may be cached on the server.
                Defaults to 300.

            is_gallery (``bool``, *optional*):
                Pass True, if results should be displayed in gallery mode instead of list mode.
                Defaults to False.

            is_personal (``bool``, *optional*):
                Pass True, if results may be cached on the server side only for the user that sent the query.
                By default (False), results may be returned to any user who sends the same query.

            next_offset (``str``, *optional*):
                Pass the offset that a client should send in the next query with the same text to receive more results.
                Pass an empty string if there are no more results or if you don‘t support pagination.
                Offset length can’t exceed 64 bytes.

            switch_pm_text (``str``, *optional*):
                If passed, clients will display a button with specified text that switches the user to a private chat
                with the bot and sends the bot a start message with the parameter switch_pm_parameter

            switch_pm_parameter (``str``, *optional*):
                `Deep-linking <https://core.telegram.org/bots#deep-linking>`_ parameter for the /start message sent to
                the bot when user presses the switch button. 1-64 characters, only A-Z, a-z, 0-9, _ and - are allowed.

                Example: An inline bot that sends YouTube videos can ask the user to connect the bot to their YouTube
                account to adapt search results accordingly. To do this, it displays a "Connect your YouTube account"
                button above the results, or even before showing any. The user presses the button, switches to a private
                chat with the bot and, in doing so, passes a start parameter that instructs the bot to return an oauth
                link. Once done, the bot can offer a switch_inline button so that the user can easily return to the chat
                where they wanted to use the bot's inline capabilities.
        """

        return await self._client.answer_inline_query(
            inline_query_id=self.id,
            results=results,
            cache_time=cache_time,
            is_gallery=is_gallery,
            is_personal=is_personal,
            next_offset=next_offset,
            switch_pm_text=switch_pm_text,
            switch_pm_parameter=switch_pm_parameter
        )

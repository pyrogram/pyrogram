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

from typing import List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class AnswerInlineQuery(Scaffold):
    async def answer_inline_query(
        self,
        inline_query_id: str,
        results: List["types.InlineQueryResult"],
        cache_time: int = 300,
        is_gallery: bool = False,
        is_personal: bool = False,
        next_offset: str = "",
        switch_pm_text: str = "",
        switch_pm_parameter: str = ""
    ):
        """Send answers to an inline query.

        A maximum of 50 results per query is allowed.

        Parameters:
            inline_query_id (``str``):
                Unique identifier for the answered query.

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

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                from pyrogram.types import InlineQueryResultArticle, InputTextMessageContent

                app.answer_inline_query(
                    inline_query_id,
                    results=[
                        InlineQueryResultArticle(
                            "Title",
                            InputTextMessageContent("Message content"))])
        """

        return await self.send(
            raw.functions.messages.SetInlineBotResults(
                query_id=int(inline_query_id),
                results=[await r.write(self) for r in results],
                cache_time=cache_time,
                gallery=is_gallery or None,
                private=is_personal or None,
                next_offset=next_offset or None,
                switch_pm=raw.types.InlineBotSwitchPM(
                    text=switch_pm_text,
                    start_param=switch_pm_parameter
                ) if switch_pm_text else None
            )
        )

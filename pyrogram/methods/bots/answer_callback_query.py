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

from pyrogram import raw
from pyrogram.scaffold import Scaffold


class AnswerCallbackQuery(Scaffold):
    async def answer_callback_query(
        self,
        callback_query_id: str,
        text: str = None,
        show_alert: bool = None,
        url: str = None,
        cache_time: int = 0
    ):
        """Send answers to callback queries sent from inline keyboards.
        The answer will be displayed to the user as a notification at the top of the chat screen or as an alert.

        Parameters:
            callback_query_id (``str``):
                Unique identifier for the query to be answered.

            text (``str`` *optional*):
                Text of the notification. If not specified, nothing will be shown to the user, 0-200 characters.

            show_alert (``bool``, *optional*):
                If true, an alert will be shown by the client instead of a notification at the top of the chat screen.
                Defaults to False.

            url (``str``, *optional*):
                URL that will be opened by the user's client.
                If you have created a Game and accepted the conditions via @Botfather, specify the URL that opens your
                game – note that this will only work if the query comes from a callback_game button.
                Otherwise, you may use links like t.me/your_bot?start=XXXX that open your bot with a parameter.

            cache_time (``int``, *optional*):
                The maximum amount of time in seconds that the result of the callback query may be cached client-side.
                Telegram apps will support caching starting in version 3.14. Defaults to 0.

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Answer only (remove the spinning circles)
                app.answer_callback_query(query_id)

                # Answer without alert
                app.answer_callback_query(query_id, text=text)

                # Answer with alert
                app.answer_callback_query(query_id, text=text, show_alert=True)
        """
        return await self.send(
            raw.functions.messages.SetBotCallbackAnswer(
                query_id=int(callback_query_id),
                cache_time=cache_time,
                alert=show_alert or None,
                message=text or None,
                url=url or None
            )
        )

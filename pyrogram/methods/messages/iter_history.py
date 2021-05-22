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

from typing import Union, Optional, AsyncGenerator

from pyrogram import types
from pyrogram.scaffold import Scaffold


class IterHistory(Scaffold):
    async def iter_history(
        self,
        chat_id: Union[int, str],
        limit: int = 0,
        offset: int = 0,
        offset_id: int = 0,
        offset_date: int = 0,
        reverse: bool = False
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat history sequentially.

        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_history` in a loop, thus saving
        you from the hassle of setting up boilerplate code. It is useful for getting the whole chat history with a
        single call.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

            offset (``int``, *optional*):
                Sequential number of the first message to be returned..
                Negative values are also accepted and become useful in case you set offset_id or offset_date.

            offset_id (``int``, *optional*):
                Identifier of the first message to be returned.

            offset_date (``int``, *optional*):
                Pass a date in Unix time as offset to retrieve only older messages starting from that date.

            reverse (``bool``, *optional*):
                Pass True to retrieve the messages in reversed order (from older to most recent).

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.

        Example:
            .. code-block:: python

                for message in app.iter_history("pyrogram"):
                    print(message.text)
        """
        offset_id = offset_id or (1 if reverse else 0)
        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        while True:
            messages = await self.get_history(
                chat_id=chat_id,
                limit=limit,
                offset=offset,
                offset_id=offset_id,
                offset_date=offset_date,
                reverse=reverse
            )

            if not messages:
                return

            offset_id = messages[-1].message_id + (1 if reverse else 0)

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return

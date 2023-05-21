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

import asyncio
from typing import Union
from functools import partial

from pyrogram import types
from pyrogram.filters import Filter


class WaitForCallbackQuery:
    async def wait_for_callback_query(
        self,
        chat_id: Union[int, str],
        filters: Filter = None,
        timeout: int = None
    ) -> "types.CallbackQuery":
        """Wait for callback query.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            filters (:obj:`Filters`):
                Pass one or more filters to allow only a subset of callback queries to be passed
                in your callback function.

            timeout (``int``, *optional*):
                Timeout in seconds.

        Returns:
            :obj:`~pyrogram.types.CallbackQuery`: On success, the callback query is returned.

        Raises:
            asyncio.TimeoutError: In case callback query not received within the timeout.

        Example:
            .. code-block:: python

                # Simple example
                callback_query = app.wait_for_callback_query(chat_id)

                # Example with filter
                callback_query = app.wait_for_callback_query(chat_id, filters=filters.user(user_id))

                # Example with timeout
                callback_query = app.wait_for_callback_query(chat_id, timeout=60)
        """

        if not isinstance(chat_id, int):
            chat = await self.get_chat(chat_id)
            chat_id = chat.id

        conversation_handler = self.dispatcher.conversation_handler
        future = self.loop.create_future()
        future.add_done_callback(
            partial(
                conversation_handler.delete_waiter,
                chat_id
            )
        )
        waiter = dict(future=future, filters=filters, update_type=types.CallbackQuery)
        conversation_handler.waiters[chat_id] = waiter
        return await asyncio.wait_for(future, timeout=timeout)

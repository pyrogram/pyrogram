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

import inspect
from typing import Union

import pyrogram
from pyrogram.types import Message, CallbackQuery
from .message_handler import MessageHandler
from .callback_query_handler import CallbackQueryHandler


class ConversationHandler(MessageHandler, CallbackQueryHandler):
    """The Conversation handler class."""
    def __init__(self):
        self.waiters = {}

    async def check(self, client: "pyrogram.Client", update: Union[Message, CallbackQuery]):
        if isinstance(update, Message) and update.outgoing:
            return False

        try:
            chat_id = update.chat.id if isinstance(update, Message) else update.message.chat.id
        except AttributeError:
            return False

        waiter = self.waiters.get(chat_id)
        if not waiter or not isinstance(update, waiter['update_type']) or waiter['future'].done():
            return False

        filters = waiter.get('filters')
        if callable(filters):
            if inspect.iscoroutinefunction(filters.__call__):
                filtered = await filters(client, update)
            else:
                filtered = await client.loop.run_in_executor(
                    client.executor,
                    filters,
                    client, update
                )
            if not filtered or waiter['future'].done():
                return False

        waiter['future'].set_result(update)
        return True

    @staticmethod
    async def callback(_, __):
        pass

    def delete_waiter(self, chat_id, future):
        if future == self.waiters[chat_id]['future']:
            del self.waiters[chat_id]

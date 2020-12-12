#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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
import logging
from collections import OrderedDict

import pyrogram
from pyrogram.api.types import (
    UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage,
    UpdateEditMessage, UpdateEditChannelMessage,
    UpdateDeleteMessages, UpdateDeleteChannelMessages,
    UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery,
    UpdateUserStatus, UpdateBotInlineQuery, UpdateMessagePoll,
    UpdateBotInlineSend
)
from . import utils
from ..handlers import (
    CallbackQueryHandler, MessageHandler, DeletedMessagesHandler,
    UserStatusHandler, RawUpdateHandler, InlineQueryHandler, PollHandler,
    ChosenInlineResultHandler
)

log = logging.getLogger(__name__)


class Dispatcher:
    NEW_MESSAGE_UPDATES = (
        UpdateNewMessage,
        UpdateNewChannelMessage,
        UpdateNewScheduledMessage
    )

    EDIT_MESSAGE_UPDATES = (
        UpdateEditMessage,
        UpdateEditChannelMessage,
    )

    DELETE_MESSAGES_UPDATES = (
        UpdateDeleteMessages,
        UpdateDeleteChannelMessages
    )

    CALLBACK_QUERY_UPDATES = (
        UpdateBotCallbackQuery,
        UpdateInlineBotCallbackQuery
    )

    MESSAGE_UPDATES = NEW_MESSAGE_UPDATES + EDIT_MESSAGE_UPDATES

    def __init__(self, client, workers: int):
        self.client = client
        self.workers = workers

        self.update_worker_tasks = []
        self.locks_list = []

        self.updates_queue = asyncio.Queue()
        self.groups = OrderedDict()

        async def message_parser(update, users, chats):
            return await pyrogram.Message._parse(
                self.client, update.message, users, chats,
                isinstance(update, UpdateNewScheduledMessage)
            ), MessageHandler

        async def deleted_messages_parser(update, users, chats):
            return utils.parse_deleted_messages(self.client, update), DeletedMessagesHandler

        async def callback_query_parser(update, users, chats):
            return await pyrogram.CallbackQuery._parse(self.client, update, users), CallbackQueryHandler

        async def user_status_parser(update, users, chats):
            return pyrogram.User._parse_user_status(self.client, update), UserStatusHandler

        async def inline_query_parser(update, users, chats):
            return pyrogram.InlineQuery._parse(self.client, update, users), InlineQueryHandler

        async def poll_parser(update, users, chats):
            return pyrogram.Poll._parse_update(self.client, update), PollHandler

        async def chosen_inline_result_parser(update, users, chats):
            return pyrogram.ChosenInlineResult._parse(self.client, update, users), ChosenInlineResultHandler

        self.update_parsers = {
            Dispatcher.MESSAGE_UPDATES: message_parser,
            Dispatcher.DELETE_MESSAGES_UPDATES: deleted_messages_parser,
            Dispatcher.CALLBACK_QUERY_UPDATES: callback_query_parser,
            (UpdateUserStatus,): user_status_parser,
            (UpdateBotInlineQuery,): inline_query_parser,
            (UpdateMessagePoll,): poll_parser,
            (UpdateBotInlineSend,): chosen_inline_result_parser
        }

        self.update_parsers = {key: value for key_tuple, value in self.update_parsers.items() for key in key_tuple}

    async def start(self):
        for i in range(self.workers):
            self.locks_list.append(asyncio.Lock())

            self.update_worker_tasks.append(
                asyncio.ensure_future(self.update_worker(self.locks_list[-1]))
            )

        logging.info("Started {} UpdateWorkerTasks".format(self.workers))

    async def stop(self):
        for i in range(self.workers):
            self.updates_queue.put_nowait(None)

        for i in self.update_worker_tasks:
            await i

        self.update_worker_tasks.clear()
        self.groups.clear()

        logging.info("Stopped {} UpdateWorkerTasks".format(self.workers))

    def add_handler(self, handler, group: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if group not in self.groups:
                    self.groups[group] = []
                    self.groups = OrderedDict(sorted(self.groups.items()))

                self.groups[group].append(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        asyncio.ensure_future(fn())

    def remove_handler(self, handler, group: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if group not in self.groups:
                    raise ValueError("Group {} does not exist. Handler was not removed.".format(group))

                self.groups[group].remove(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        asyncio.ensure_future(fn())

    async def update_worker(self, lock):
        while True:
            packet = await self.updates_queue.get()

            if packet is None:
                break

            try:
                update, users, chats = packet
                parser = self.update_parsers.get(type(update), None)

                parsed_update, handler_type = (
                    await parser(update, users, chats)
                    if parser is not None
                    else (None, type(None))
                )

                async with lock:
                    for group in self.groups.values():
                        for handler in group:
                            args = None

                            if isinstance(handler, handler_type):
                                try:
                                    if handler.check(parsed_update):
                                        args = (parsed_update,)
                                except Exception as e:
                                    log.error(e, exc_info=True)
                                    continue

                            elif isinstance(handler, RawUpdateHandler):
                                args = (update, users, chats)

                            if args is None:
                                continue

                            try:
                                await handler.callback(self.client, *args)
                            except pyrogram.StopPropagation:
                                raise
                            except pyrogram.ContinuePropagation:
                                continue
                            except Exception as e:
                                log.error(e, exc_info=True)

                            break
            except pyrogram.StopPropagation:
                pass
            except Exception as e:
                log.error(e, exc_info=True)

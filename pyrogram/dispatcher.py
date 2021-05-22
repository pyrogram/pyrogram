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

import asyncio
import inspect
import logging
from collections import OrderedDict

import pyrogram
from pyrogram import utils
from pyrogram.handlers import (
    CallbackQueryHandler, MessageHandler, DeletedMessagesHandler,
    UserStatusHandler, RawUpdateHandler, InlineQueryHandler, PollHandler,
    ChosenInlineResultHandler, ChatMemberUpdatedHandler
)
from pyrogram.raw.types import (
    UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage,
    UpdateEditMessage, UpdateEditChannelMessage,
    UpdateDeleteMessages, UpdateDeleteChannelMessages,
    UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery,
    UpdateUserStatus, UpdateBotInlineQuery, UpdateMessagePoll,
    UpdateBotInlineSend, UpdateChatParticipant, UpdateChannelParticipant
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

    CHAT_MEMBER_UPDATES = (
        UpdateChatParticipant,
        UpdateChannelParticipant
    )

    MESSAGE_UPDATES = NEW_MESSAGE_UPDATES + EDIT_MESSAGE_UPDATES

    def __init__(self, client: "pyrogram.Client"):
        self.client = client
        self.loop = asyncio.get_event_loop()

        self.handler_worker_tasks = []
        self.locks_list = []

        self.updates_queue = asyncio.Queue()
        self.groups = OrderedDict()

        async def message_parser(update, users, chats):
            return await pyrogram.types.Message._parse(
                self.client, update.message, users, chats,
                isinstance(update, UpdateNewScheduledMessage)
            ), MessageHandler

        async def deleted_messages_parser(update, users, chats):
            return utils.parse_deleted_messages(self.client, update), DeletedMessagesHandler

        async def callback_query_parser(update, users, chats):
            return await pyrogram.types.CallbackQuery._parse(self.client, update, users), CallbackQueryHandler

        async def user_status_parser(update, users, chats):
            return pyrogram.types.User._parse_user_status(self.client, update), UserStatusHandler

        async def inline_query_parser(update, users, chats):
            return pyrogram.types.InlineQuery._parse(self.client, update, users), InlineQueryHandler

        async def poll_parser(update, users, chats):
            return pyrogram.types.Poll._parse_update(self.client, update), PollHandler

        async def chosen_inline_result_parser(update, users, chats):
            return pyrogram.types.ChosenInlineResult._parse(self.client, update, users), ChosenInlineResultHandler

        async def chat_member_updated_parser(update, users, chats):
            return pyrogram.types.ChatMemberUpdated._parse(self.client, update, users, chats), ChatMemberUpdatedHandler

        self.update_parsers = {
            Dispatcher.MESSAGE_UPDATES: message_parser,
            Dispatcher.DELETE_MESSAGES_UPDATES: deleted_messages_parser,
            Dispatcher.CALLBACK_QUERY_UPDATES: callback_query_parser,
            (UpdateUserStatus,): user_status_parser,
            (UpdateBotInlineQuery,): inline_query_parser,
            (UpdateMessagePoll,): poll_parser,
            (UpdateBotInlineSend,): chosen_inline_result_parser,
            Dispatcher.CHAT_MEMBER_UPDATES: chat_member_updated_parser
        }

        self.update_parsers = {key: value for key_tuple, value in self.update_parsers.items() for key in key_tuple}

    async def start(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.locks_list.append(asyncio.Lock())

                self.handler_worker_tasks.append(
                    self.loop.create_task(self.handler_worker(self.locks_list[-1]))
                )

            log.info(f"Started {self.client.workers} HandlerTasks")

    async def stop(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.updates_queue.put_nowait(None)

            for i in self.handler_worker_tasks:
                await i

            self.handler_worker_tasks.clear()
            self.groups.clear()

            log.info(f"Stopped {self.client.workers} HandlerTasks")

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

        self.loop.create_task(fn())

    def remove_handler(self, handler, group: int):
        async def fn():
            for lock in self.locks_list:
                await lock.acquire()

            try:
                if group not in self.groups:
                    raise ValueError(f"Group {group} does not exist. Handler was not removed.")

                self.groups[group].remove(handler)
            finally:
                for lock in self.locks_list:
                    lock.release()

        self.loop.create_task(fn())

    async def handler_worker(self, lock):
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
                                    if await handler.check(self.client, parsed_update):
                                        args = (parsed_update,)
                                except Exception as e:
                                    log.error(e, exc_info=True)
                                    continue

                            elif isinstance(handler, RawUpdateHandler):
                                args = (update, users, chats)

                            if args is None:
                                continue

                            try:
                                if inspect.iscoroutinefunction(handler.callback):
                                    await handler.callback(self.client, *args)
                                else:
                                    await self.loop.run_in_executor(
                                        self.client.executor,
                                        handler.callback,
                                        self.client,
                                        *args
                                    )
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

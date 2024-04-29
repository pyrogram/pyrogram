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
import inspect
import logging
from collections import OrderedDict

import pyrogram
from pyrogram import errors
from pyrogram import utils
from pyrogram import raw
from pyrogram.handlers import (
    CallbackQueryHandler, MessageHandler, EditedMessageHandler, DeletedMessagesHandler,
    UserStatusHandler, RawUpdateHandler, InlineQueryHandler, PollHandler,
    ChosenInlineResultHandler, ChatMemberUpdatedHandler, ChatJoinRequestHandler, StoryHandler
)
from pyrogram.raw.types import (
    UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage,
    UpdateBotNewBusinessMessage, UpdateBotEditBusinessMessage, UpdateBotDeleteBusinessMessage,
    UpdateEditMessage, UpdateEditChannelMessage,
    UpdateDeleteMessages, UpdateDeleteChannelMessages,
    UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery,
    UpdateUserStatus, UpdateBotInlineQuery, UpdateMessagePoll,
    UpdateBotInlineSend, UpdateChatParticipant, UpdateChannelParticipant,
    UpdateBotChatInviteRequester, UpdateStory
)

log = logging.getLogger(__name__)


class Dispatcher:
    NEW_MESSAGE_UPDATES = (UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage)
    EDIT_MESSAGE_UPDATES = (UpdateEditMessage, UpdateEditChannelMessage)
    DELETE_MESSAGES_UPDATES = (UpdateDeleteMessages, UpdateDeleteChannelMessages)
    CALLBACK_QUERY_UPDATES = (UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery)
    CHAT_MEMBER_UPDATES = (UpdateChatParticipant, UpdateChannelParticipant)
    USER_STATUS_UPDATES = (UpdateUserStatus,)
    BOT_INLINE_QUERY_UPDATES = (UpdateBotInlineQuery,)
    POLL_UPDATES = (UpdateMessagePoll,)
    CHOSEN_INLINE_RESULT_UPDATES = (UpdateBotInlineSend,)
    CHAT_JOIN_REQUEST_UPDATES = (UpdateBotChatInviteRequester,)
    NEW_STORY_UPDATES = (UpdateStory,)
    BOT_NEW_BUSINESS_MESSAGE_UPDATES = (UpdateBotNewBusinessMessage,)
    BOT_EDIT_BUSINESS_MESSAGE_UPDATES = (UpdateBotEditBusinessMessage,)
    BOT_DELETE_BUSINESS_MESSAGE_UPDATES = (UpdateBotDeleteBusinessMessage,)

    def __init__(self, client: "pyrogram.Client"):
        self.client = client
        self.loop = asyncio.get_event_loop()

        self.handler_worker_tasks = []
        self.locks_list = []

        self.updates_queue = asyncio.Queue()
        self.groups = OrderedDict()

        async def message_parser(update, users, chats):
            return (
                await pyrogram.types.Message._parse(
                    self.client,
                    update.message,
                    users,
                    chats,
                    is_scheduled=isinstance(update, UpdateNewScheduledMessage),
                    business_connection_id=getattr(update, "connection_id", None),
                    reply_to_message=getattr(update, "reply_to_message", None)
                ),
                MessageHandler
            )

        async def edited_message_parser(update, users, chats):
            # Edited messages are parsed the same way as new messages, but the handler is different
            parsed, _ = await message_parser(update, users, chats)

            return (
                parsed,
                EditedMessageHandler
            )

        async def deleted_messages_parser(update, users, chats):
            return (
                utils.parse_deleted_messages(self.client, update, users, chats),
                DeletedMessagesHandler,
            )

        async def callback_query_parser(update, users, chats):
            return (
                await pyrogram.types.CallbackQuery._parse(self.client, update, users),
                CallbackQueryHandler
            )

        async def user_status_parser(update, users, chats):
            return (
                pyrogram.types.User._parse_user_status(self.client, update),
                UserStatusHandler
            )

        async def inline_query_parser(update, users, chats):
            return (
                pyrogram.types.InlineQuery._parse(self.client, update, users),
                InlineQueryHandler
            )

        async def poll_parser(update, users, chats):
            return (
                pyrogram.types.Poll._parse_update(self.client, update),
                PollHandler
            )

        async def chosen_inline_result_parser(update, users, chats):
            return (
                pyrogram.types.ChosenInlineResult._parse(self.client, update, users),
                ChosenInlineResultHandler
            )

        async def chat_member_updated_parser(update, users, chats):
            return (
                pyrogram.types.ChatMemberUpdated._parse(self.client, update, users, chats),
                ChatMemberUpdatedHandler
            )

        async def chat_join_request_parser(update, users, chats):
            return (
                pyrogram.types.ChatJoinRequest._parse(self.client, update, users, chats),
                ChatJoinRequestHandler
            )

        async def story_parser(update, users, chats):
            return (
                await pyrogram.types.Story._parse(self.client, update.story, users, chats, update.peer),
                StoryHandler
            )

        self.update_parsers = {
            Dispatcher.NEW_MESSAGE_UPDATES: message_parser,
            Dispatcher.EDIT_MESSAGE_UPDATES: edited_message_parser,
            Dispatcher.DELETE_MESSAGES_UPDATES: deleted_messages_parser,
            Dispatcher.CALLBACK_QUERY_UPDATES: callback_query_parser,
            Dispatcher.USER_STATUS_UPDATES: user_status_parser,
            Dispatcher.BOT_INLINE_QUERY_UPDATES: inline_query_parser,
            Dispatcher.POLL_UPDATES: poll_parser,
            Dispatcher.CHOSEN_INLINE_RESULT_UPDATES: chosen_inline_result_parser,
            Dispatcher.CHAT_MEMBER_UPDATES: chat_member_updated_parser,
            Dispatcher.CHAT_JOIN_REQUEST_UPDATES: chat_join_request_parser,
            Dispatcher.NEW_STORY_UPDATES: story_parser,
            Dispatcher.BOT_NEW_BUSINESS_MESSAGE_UPDATES: message_parser,
            Dispatcher.BOT_EDIT_BUSINESS_MESSAGE_UPDATES: edited_message_parser,
            Dispatcher.BOT_DELETE_BUSINESS_MESSAGE_UPDATES: deleted_messages_parser,
        }

        self.update_parsers = {key: value for key_tuple, value in self.update_parsers.items() for key in key_tuple}

    async def start(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.locks_list.append(asyncio.Lock())

                self.handler_worker_tasks.append(
                    self.loop.create_task(self.handler_worker(self.locks_list[-1]))
                )

            log.info("Started %s HandlerTasks", self.client.workers)

            if not self.client.skip_updates:
                states = await self.client.storage.update_state()

                if not states:
                    log.info("No states found, skipping recovery.")
                    return

                message_updates_counter = 0
                other_updates_counter = 0

                for state in states:
                    id, local_pts, _, local_date, _ = state

                    prev_pts = 0

                    while True:
                        try:
                            diff = await self.client.invoke(
                                raw.functions.updates.GetChannelDifference(
                                    channel=await self.client.resolve_peer(id),
                                    filter=raw.types.ChannelMessagesFilterEmpty(),
                                    pts=local_pts,
                                    limit=10000
                                ) if id < 0 else
                                raw.functions.updates.GetDifference(
                                    pts=local_pts,
                                    date=local_date,
                                    qts=0
                                )
                            )
                        except (errors.ChannelPrivate, errors.ChannelInvalid):
                            break

                        if isinstance(diff, raw.types.updates.DifferenceEmpty):
                            break
                        elif isinstance(diff, raw.types.updates.DifferenceTooLong):
                            break
                        elif isinstance(diff, raw.types.updates.Difference):
                            local_pts = diff.state.pts
                        elif isinstance(diff, raw.types.updates.DifferenceSlice):
                            local_pts = diff.intermediate_state.pts
                            local_date = diff.intermediate_state.date

                            if prev_pts == local_pts:
                                break

                            prev_pts = local_pts
                        elif isinstance(diff, raw.types.updates.ChannelDifferenceEmpty):
                            break
                        elif isinstance(diff, raw.types.updates.ChannelDifferenceTooLong):
                            break
                        elif isinstance(diff, raw.types.updates.ChannelDifference):
                            local_pts = diff.pts

                        users = {i.id: i for i in diff.users}
                        chats = {i.id: i for i in diff.chats}

                        for message in diff.new_messages:
                            message_updates_counter += 1
                            self.updates_queue.put_nowait(
                                (
                                    raw.types.UpdateNewMessage(
                                        message=message,
                                        pts=local_pts,
                                        pts_count=-1
                                    ) if id == self.client.me.id else
                                    raw.types.UpdateNewChannelMessage(
                                        message=message,
                                        pts=local_pts,
                                        pts_count=-1
                                    ),
                                    users,
                                    chats
                                )
                            )

                        for update in diff.other_updates:
                            other_updates_counter += 1
                            self.updates_queue.put_nowait(
                                (update, users, chats)
                            )

                        if isinstance(diff, (raw.types.updates.Difference, raw.types.updates.ChannelDifference)):
                            break

                    await self.client.storage.update_state(id)

                log.info("Recovered %s messages and %s updates.", message_updates_counter, other_updates_counter)

    async def stop(self):
        if not self.client.no_updates:
            for i in range(self.client.workers):
                self.updates_queue.put_nowait(None)

            for i in self.handler_worker_tasks:
                await i

            self.handler_worker_tasks.clear()
            self.groups.clear()

            log.info("Stopped %s HandlerTasks", self.client.workers)

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
                                    log.exception(e)
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
                                log.exception(e)

                            break
            except pyrogram.StopPropagation:
                pass
            except Exception as e:
                log.exception(e)

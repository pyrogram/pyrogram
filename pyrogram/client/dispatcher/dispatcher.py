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

import logging
import threading
from collections import OrderedDict
from queue import Queue
from threading import Thread

import pyrogram
from pyrogram.api import types
from ..ext import utils
from ..handlers import CallbackQueryHandler, MessageHandler, DeletedMessagesHandler, UserStatusHandler, RawUpdateHandler

log = logging.getLogger(__name__)


class Dispatcher:
    NEW_MESSAGE_UPDATES = (
        types.UpdateNewMessage,
        types.UpdateNewChannelMessage
    )

    EDIT_MESSAGE_UPDATES = (
        types.UpdateEditMessage,
        types.UpdateEditChannelMessage
    )

    DELETE_MESSAGE_UPDATES = (
        types.UpdateDeleteMessages,
        types.UpdateDeleteChannelMessages
    )

    MESSAGE_UPDATES = NEW_MESSAGE_UPDATES + EDIT_MESSAGE_UPDATES

    def __init__(self, client, workers):
        self.client = client
        self.workers = workers
        self.workers_list = []
        self.updates = Queue()
        self.groups = OrderedDict()

    def start(self):
        for i in range(self.workers):
            self.workers_list.append(
                Thread(
                    target=self.update_worker,
                    name="UpdateWorker#{}".format(i + 1)
                )
            )

            self.workers_list[-1].start()

    def stop(self):
        for _ in range(self.workers):
            self.updates.put(None)

        for i in self.workers_list:
            i.join()

        self.workers_list.clear()

    def add_handler(self, handler, group: int):
        if group not in self.groups:
            self.groups[group] = []
            self.groups = OrderedDict(sorted(self.groups.items()))

        self.groups[group].append(handler)

    def remove_handler(self, handler, group: int):
        if group not in self.groups:
            raise ValueError("Group {} does not exist. "
                             "Handler was not removed.".format(group))
        self.groups[group].remove(handler)

    def update_worker(self):
        name = threading.current_thread().name
        log.debug("{} started".format(name))

        while True:
            update = self.updates.get()

            if update is None:
                break

            try:
                users = {i.id: i for i in update[1]}
                chats = {i.id: i for i in update[2]}
                update = update[0]

                self.dispatch_raw(update, users=users, chats=chats, handler_class=RawUpdateHandler)

                if isinstance(update, Dispatcher.MESSAGE_UPDATES):
                    if isinstance(update.message, types.MessageEmpty):
                        continue

                    message = utils.parse_messages(self.client, update.message, users, chats)
                    is_edited = isinstance(update, Dispatcher.EDIT_MESSAGE_UPDATES)
                    is_channel = message.chat.type == "channel"

                    update = pyrogram.Update(
                        message=message if not is_channel and not is_edited else None,
                        edited_message=message if not is_channel and is_edited else None,
                        channel_post=message if is_channel and not is_edited else None,
                        edited_channel_post=message if is_channel and is_edited else None
                    )

                elif isinstance(update, Dispatcher.DELETE_MESSAGE_UPDATES):
                    is_channel = hasattr(update, "channel_id")
                    messages = utils.parse_deleted_messages(
                        update.messages,
                        update.channel_id if is_channel else None
                    )

                    update = pyrogram.Update(
                        deleted_messages=messages if not is_channel else None,
                        deleted_channel_posts=messages if is_channel else None
                    )

                elif isinstance(update, types.UpdateBotCallbackQuery):
                    update = pyrogram.Update(
                        callback_query=utils.parse_callback_query(
                            self.client, update, users
                        )
                    )
                elif isinstance(update, types.UpdateInlineBotCallbackQuery):
                    update = pyrogram.Update(
                        callback_query=utils.parse_inline_callback_query(
                            self.client, update, users
                        )
                    )
                elif isinstance(update, types.UpdateUserStatus):
                    update = pyrogram.Update(
                        user_status=utils.parse_user_status(
                            update.status, update.user_id
                        )
                    )
                else:
                    continue

                self.dispatch(update)
            except Exception as e:
                log.error(e, exc_info=True)

        log.debug("{} stopped".format(name))

    def dispatch_raw(self, update, users: dict, chats: dict, handler_class):
        for group in self.groups.values():
            for handler in group:
                if isinstance(handler, handler_class):
                    try:
                        handler.callback(self.client, update, users, chats)
                    except Exception as e:
                        log.error(e, exc_info=True)

    # noinspection PyShadowingBuiltins
    def dispatch(self, update):
        message = update.message or update.channel_post or update.edited_message or update.edited_channel_post
        deleted_messages = update.deleted_channel_posts or update.deleted_messages
        callback_query = update.callback_query
        user_status = update.user_status

        update = message or deleted_messages or callback_query or user_status

        type = (
            MessageHandler if message
            else DeletedMessagesHandler if deleted_messages
            else CallbackQueryHandler if callback_query
            else UserStatusHandler if user_status
            else None
        )

        for group in self.groups.values():
            for handler in group:
                if isinstance(handler, type):
                    if handler.check(update):
                        try:
                            handler.callback(self.client, update)
                        except Exception as e:
                            log.error(e, exc_info=True)

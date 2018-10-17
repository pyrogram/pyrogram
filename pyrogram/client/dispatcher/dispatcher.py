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
                    update = message, MessageHandler

                elif isinstance(update, Dispatcher.DELETE_MESSAGE_UPDATES):
                    deleted_messages = utils.parse_deleted_messages(
                        update.messages,
                        update.channel_id if hasattr(update, "channel_id") else None
                    )

                    update = deleted_messages, DeletedMessagesHandler

                elif isinstance(update, types.UpdateBotCallbackQuery):
                    update = utils.parse_callback_query(self.client, update, users), CallbackQueryHandler
                elif isinstance(update, types.UpdateInlineBotCallbackQuery):
                    update = utils.parse_inline_callback_query(self.client, update, users), CallbackQueryHandler
                elif isinstance(update, types.UpdateUserStatus):
                    update = utils.parse_user_status(update.status, update.user_id), UserStatusHandler
                else:
                    continue

                self.dispatch(*update)
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
    def dispatch(self, update, handler_class):
        for group in self.groups.values():
            for handler in group:
                if isinstance(handler, handler_class):
                    if handler.check(update):
                        try:
                            handler.callback(self.client, update)
                        except Exception as e:
                            log.error(e, exc_info=True)

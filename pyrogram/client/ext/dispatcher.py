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

import logging
import threading
from collections import OrderedDict
from queue import Queue
from threading import Thread, Lock

import pyrogram
from pyrogram.api.types import (
    UpdateNewMessage, UpdateNewChannelMessage, UpdateNewScheduledMessage,
    UpdateEditMessage, UpdateEditChannelMessage,
    UpdateDeleteMessages, UpdateDeleteChannelMessages,
    UpdateBotCallbackQuery, UpdateInlineBotCallbackQuery,
    UpdateUserStatus, UpdateBotInlineQuery, UpdateMessagePoll
)
from . import utils
from ..handlers import (
    CallbackQueryHandler, MessageHandler, DeletedMessagesHandler,
    UserStatusHandler, RawUpdateHandler, InlineQueryHandler, PollHandler
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

        self.workers_list = []
        self.locks_list = []

        self.updates_queue = Queue()
        self.groups = OrderedDict()

        self.update_parsers = {
            Dispatcher.MESSAGE_UPDATES:
                lambda upd, usr, cht: (
                    pyrogram.Message._parse(
                        self.client,
                        upd.message,
                        usr,
                        cht,
                        isinstance(upd, UpdateNewScheduledMessage)
                    ),
                    MessageHandler
                ),

            Dispatcher.DELETE_MESSAGES_UPDATES:
                lambda upd, usr, cht: (utils.parse_deleted_messages(self.client, upd), DeletedMessagesHandler),

            Dispatcher.CALLBACK_QUERY_UPDATES:
                lambda upd, usr, cht: (pyrogram.CallbackQuery._parse(self.client, upd, usr), CallbackQueryHandler),

            (UpdateUserStatus,):
                lambda upd, usr, cht: (pyrogram.User._parse_user_status(self.client, upd), UserStatusHandler),

            (UpdateBotInlineQuery,):
                lambda upd, usr, cht: (pyrogram.InlineQuery._parse(self.client, upd, usr), InlineQueryHandler),

            (UpdateMessagePoll,):
                lambda upd, usr, cht: (pyrogram.Poll._parse_update(self.client, upd), PollHandler)
        }

        self.update_parsers = {key: value for key_tuple, value in self.update_parsers.items() for key in key_tuple}

    def start(self):
        for i in range(self.workers):
            self.locks_list.append(Lock())

            self.workers_list.append(
                Thread(
                    target=self.update_worker,
                    name="UpdateWorker#{}".format(i + 1),
                    args=(self.locks_list[-1],)
                )
            )

            self.workers_list[-1].start()

    def stop(self):
        for _ in range(self.workers):
            self.updates_queue.put(None)

        for worker in self.workers_list:
            worker.join()

        self.workers_list.clear()
        self.locks_list.clear()
        self.groups.clear()

    def add_handler(self, handler, group: int):
        for lock in self.locks_list:
            lock.acquire()

        try:
            if group not in self.groups:
                self.groups[group] = []
                self.groups = OrderedDict(sorted(self.groups.items()))

            self.groups[group].append(handler)
        finally:
            for lock in self.locks_list:
                lock.release()

    def remove_handler(self, handler, group: int):
        for lock in self.locks_list:
            lock.acquire()

        try:
            if group not in self.groups:
                raise ValueError("Group {} does not exist. Handler was not removed.".format(group))

            self.groups[group].remove(handler)
        finally:
            for lock in self.locks_list:
                lock.release()

    def update_worker(self, lock):
        name = threading.current_thread().name
        log.debug("{} started".format(name))

        while True:
            packet = self.updates_queue.get()

            if packet is None:
                break

            try:
                update, users, chats = packet
                parser = self.update_parsers.get(type(update), None)

                parsed_update, handler_type = (
                    parser(update, users, chats)
                    if parser is not None
                    else (None, type(None))
                )

                with lock:
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
                                handler.callback(self.client, *args)
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

        log.debug("{} stopped".format(name))

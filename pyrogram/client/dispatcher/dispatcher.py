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
from .. import message_parser
from ..handler import (
    Handler, MessageHandler, RawUpdateHandler
)

log = logging.getLogger(__name__)


class Dispatcher:
    MESSAGE_UPDATES = (
        types.UpdateNewMessage,
        types.UpdateNewChannelMessage
    )

    EDIT_UPDATES = (
        types.UpdateEditMessage,
        types.UpdateEditChannelMessage
    )

    ALLOWED_UPDATES = MESSAGE_UPDATES + EDIT_UPDATES

    def __init__(self, client, workers):
        self.client = client
        self.workers = workers
        self.updates = Queue()
        self.handlers = OrderedDict()

    def start(self):
        for i in range(self.workers):
            Thread(
                target=self.update_worker,
                name="UpdateWorker#{}".format(i + 1)
            ).start()

    def stop(self):
        for _ in range(self.workers):
            self.updates.put(None)

    def add_handler(self, handler: Handler, group: int):
        if group not in self.handlers:
            self.handlers[group] = {}
            self.handlers = OrderedDict(sorted(self.handlers.items()))

        if type(handler) not in self.handlers[group]:
            self.handlers[group][type(handler)] = handler
        else:
            raise ValueError(
                "'{0}' is already registered in Group #{1}. "
                "You can register a different handler in this group "
                "or another '{0}' in a different group".format(
                    type(handler).__name__,
                    group
                )
            )

    def dispatch(self, update, users: dict = None, chats: dict = None, is_raw: bool = False):
        if is_raw:
            key = RawUpdateHandler
            value = update
        else:
            message = (update.message
                       or update.channel_post
                       or update.edited_message
                       or update.edited_channel_post)

            if message:
                key = MessageHandler
                value = message
            else:
                return

        for group in self.handlers.values():
            handler = group.get(key, None)

            if handler is not None:
                args = (self, value, users, chats) if is_raw else (self.client, value)
                handler.callback(*args)

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

                self.dispatch(update, users=users, chats=chats, is_raw=True)

                if isinstance(update, Dispatcher.ALLOWED_UPDATES):
                    if isinstance(update.message, types.Message):
                        parser = message_parser.parse_message
                    elif isinstance(update.message, types.MessageService):
                        parser = message_parser.parse_message_service
                    else:
                        continue

                    message = parser(
                        self.client,
                        update.message,
                        users,
                        chats
                    )
                else:
                    continue

                is_edited_message = isinstance(update, Dispatcher.EDIT_UPDATES)

                self.dispatch(
                    pyrogram.Update(
                        update_id=0,
                        message=((message if message.chat.type != "channel"
                                  else None) if not is_edited_message
                                 else None),
                        edited_message=((message if message.chat.type != "channel"
                                         else None) if is_edited_message
                                        else None),
                        channel_post=((message if message.chat.type == "channel"
                                       else None) if not is_edited_message
                                      else None),
                        edited_channel_post=((message if message.chat.type == "channel"
                                              else None) if is_edited_message
                                             else None)
                    )
                )
            except Exception as e:
                log.error(e, exc_info=True)

        log.debug("{} stopped".format(name))

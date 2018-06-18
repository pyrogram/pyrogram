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

import asyncio
import logging
from collections import OrderedDict

import pyrogram
from pyrogram.api import types
from ..ext import utils
from ..handlers import RawUpdateHandler, CallbackQueryHandler, MessageHandler

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

    MESSAGE_UPDATES = NEW_MESSAGE_UPDATES + EDIT_MESSAGE_UPDATES

    def __init__(self, client, workers):
        self.client = client
        self.workers = workers

        self.update_worker_tasks = []
        self.updates = asyncio.Queue()
        self.groups = OrderedDict()

    async def start(self):
        for i in range(self.workers):
            self.update_worker_tasks.append(
                asyncio.ensure_future(self.update_worker())
            )

        log.info("Started {} UpdateWorkerTasks".format(self.workers))

    async def stop(self):
        for i in range(self.workers):
            self.updates.put_nowait(None)

        for i in self.update_worker_tasks:
            await i

        self.update_worker_tasks.clear()

        log.info("Stopped {} UpdateWorkerTasks".format(self.workers))

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

    async def dispatch(self, update, users: dict = None, chats: dict = None, is_raw: bool = False):
        tasks = []

        for group in self.groups.values():
            for handler in group:
                if is_raw:
                    if not isinstance(handler, RawUpdateHandler):
                        continue

                    args = (self.client, update, users, chats)
                else:
                    message = (update.message
                               or update.channel_post
                               or update.edited_message
                               or update.edited_channel_post)

                    callback_query = update.callback_query

                    if message and isinstance(handler, MessageHandler):
                        if not handler.check(message):
                            continue

                        args = (self.client, message)
                    elif callback_query and isinstance(handler, CallbackQueryHandler):
                        if not handler.check(callback_query):
                            continue

                        args = (self.client, callback_query)
                    else:
                        continue

                tasks.append(handler.callback(*args))
                break

        await asyncio.gather(*tasks)

    async def update_worker(self):
        while True:
            update = await self.updates.get()

            if update is None:
                break

            try:
                users = {i.id: i for i in update[1]}
                chats = {i.id: i for i in update[2]}
                update = update[0]

                await self.dispatch(update, users=users, chats=chats, is_raw=True)

                if isinstance(update, Dispatcher.MESSAGE_UPDATES):
                    if isinstance(update.message, types.MessageEmpty):
                        continue

                    message = await utils.parse_messages(
                        self.client,
                        update.message,
                        users,
                        chats
                    )

                    is_edited_message = isinstance(update, Dispatcher.EDIT_MESSAGE_UPDATES)

                    await self.dispatch(
                        pyrogram.Update(
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
                elif isinstance(update, types.UpdateBotCallbackQuery):
                    await self.dispatch(
                        pyrogram.Update(
                            callback_query=await utils.parse_callback_query(
                                self.client, update, users
                            )
                        )
                    )
                elif isinstance(update, types.UpdateInlineBotCallbackQuery):
                    await self.dispatch(
                        pyrogram.Update(
                            callback_query=await utils.parse_inline_callback_query(
                                update, users
                            )
                        )
                    )
                else:
                    continue
            except Exception as e:
                log.error(e, exc_info=True)

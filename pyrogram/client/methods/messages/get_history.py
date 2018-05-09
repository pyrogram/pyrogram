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

from pyrogram.api import functions, types
from ...ext import BaseClient, utils


class GetHistory(BaseClient):
    def get_history(self,
                    chat_id: int or str,
                    offset: int,
                    limit: int,
                    offset_id: int = 0,
                    offset_date: int = 0,
                    max_id: int = 0,
                    min_id: int = 0):
        # TODO: Documentation

        r = self.send(
            functions.messages.GetHistory(
                peer=self.resolve_peer(chat_id),
                offset_id=offset_id,
                offset_date=offset_date,
                add_offset=offset,
                limit=limit,
                max_id=max_id,
                min_id=min_id,
                hash=0
            )
        )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        messages = []

        for i in r.messages:
            if isinstance(i, types.Message):
                messages.append(
                    utils.parse_message(
                        self, i, users, chats
                    )
                )
            elif isinstance(i, types.MessageService):
                messages.append(
                    utils.parse_message_service(
                        self, i, users, chats
                    )
                )
            else:
                messages.append(
                    utils.parse_message_empty(
                        self, i
                    )
                )

        return messages

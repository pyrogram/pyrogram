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

import pyrogram
from pyrogram.api import functions
from ...ext import BaseClient, utils


class GetHistory(BaseClient):
    def get_history(self,
                    chat_id: int or str,
                    offset: int = 0,
                    limit: int = 100,
                    offset_id: int = 0,
                    offset_date: int = 0):
        """Use this method to retrieve the history of a chat.

        You can get up to 100 messages at once.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                For a private channel/supergroup you can use its *t.me/joinchat/* link.

            offset (``int``, *optional*)
                Sequential number of the first message to be returned.
                Defaults to 0 (most recent message).

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, the first 100 messages are returned.

            offset_id (``int``, *optional*):
                Pass a message identifier as offset to retrieve only older messages starting from that message.

            offset_date (``int``, *optional*):
                Pass a date in Unix time as offset to retrieve only older messages starting from that date.

        Returns:
            On success, a :obj:`Messages <pyrogram.Messages>` object is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
        """

        r = self.send(
            functions.messages.GetHistory(
                peer=self.resolve_peer(chat_id),
                offset_id=offset_id,
                offset_date=offset_date,
                add_offset=offset,
                limit=limit,
                max_id=0,
                min_id=0,
                hash=0
            )
        )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        reply_to_messages = {
            i.reply_to_msg_id: None
            for i in r.messages
            if i.reply_to_msg_id
        }

        if reply_to_messages:
            temp = self.get_messages(
                chat_id, reply_to_messages,
                replies=0
            )

            assert len(temp) == len(reply_to_messages)

            for i in range(len(temp)):
                reply_to_messages[temp[i].message_id] = temp[i]

        messages = utils.parse_messages(
            self, r.messages,
            users, chats,
            replies=0
        )

        assert len(messages) == len(r.messages)

        for i in range(len(messages)):
            if r.messages[i].reply_to_msg_id:
                messages[i].reply_to_message = reply_to_messages[r.messages[i].reply_to_msg_id]

        return pyrogram.Messages(
            total_count=getattr(r, "count", len(r.messages)),
            messages=messages
        )

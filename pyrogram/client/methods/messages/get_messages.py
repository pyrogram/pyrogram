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


class GetMessages(BaseClient):
    def get_messages(self,
                     chat_id: int or str,
                     message_ids,
                     replies: int = 1):
        """Use this method to get messages that belong to a specific chat.
        You can retrieve up to 200 messages at once.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                For a private channel/supergroup you can use its *t.me/joinchat/* link.

            message_ids (``iterable``):
                A list of Message identifiers in the chat specified in *chat_id* or a single message id, as integer.
                Iterators and Generators are also accepted.

            replies (``int``, *optional*):
                The number of subsequent replies to get for each message. Defaults to 1.

        Returns:
            On success and in case *message_ids* was a list, the returned value will be a list of the requested
            :obj:`Messages <pyrogram.Message>` even if a list contains just one element, otherwise if
            *message_ids* was an integer, the single requested :obj:`Message <pyrogram.Message>`
            is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        peer = self.resolve_peer(chat_id)
        is_iterable = not isinstance(message_ids, int)
        message_ids = list(message_ids) if is_iterable else [message_ids]
        message_ids = [types.InputMessageID(i) for i in message_ids]

        if isinstance(peer, types.InputPeerChannel):
            rpc = functions.channels.GetMessages(
                channel=peer,
                id=message_ids
            )
        else:
            rpc = functions.messages.GetMessages(
                id=message_ids
            )

        r = self.send(rpc)

        messages = utils.parse_messages(
            self, r.messages,
            {i.id: i for i in r.users},
            {i.id: i for i in r.chats},
            replies=replies
        )

        return messages if is_iterable else messages[0]

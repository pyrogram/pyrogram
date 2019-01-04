# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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
import time
from typing import Union, Iterable

import pyrogram
from pyrogram.api import functions, types
from pyrogram.api.errors import FloodWait
from ...ext import BaseClient

log = logging.getLogger(__name__)


class GetMessages(BaseClient):
    def get_messages(self,
                     chat_id: Union[int, str],
                     message_ids: Union[int, Iterable[int]] = None,
                     reply_to_message_ids: Union[int, Iterable[int]] = None,
                     replies: int = 1) -> "pyrogram.Messages":
        """Use this method to get one or more messages that belong to a specific chat.
        You can retrieve up to 200 messages at once.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``iterable``, *optional*):
                Pass a single message identifier or a list of message ids (as integers) to get the content of the
                message themselves. Iterators and Generators are also accepted.

            reply_to_message_ids (``iterable``, *optional*):
                Pass a single message identifier or a list of message ids (as integers) to get the content of
                the previous message you replied to using this message. Iterators and Generators are also accepted.
                If *message_ids* is set, this argument will be ignored.

            replies (``int``, *optional*):
                The number of subsequent replies to get for each message. Defaults to 1.

        Returns:
            On success and in case *message_ids* or *reply_to_message_ids* was an iterable, the returned value will be a
            :obj:`Messages <pyrogram.Messages>` even if a list contains just one element. Otherwise, if *message_ids* or
            *reply_to_message_ids* was an integer, the single requested :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """
        ids, ids_type = (
            (message_ids, types.InputMessageID) if message_ids
            else (reply_to_message_ids, types.InputMessageReplyTo) if reply_to_message_ids
            else (None, None)
        )

        if ids is None:
            raise ValueError("No argument supplied")

        peer = self.resolve_peer(chat_id)

        is_iterable = not isinstance(ids, int)
        ids = list(ids) if is_iterable else [ids]
        ids = [ids_type(i) for i in ids]

        if isinstance(peer, types.InputPeerChannel):
            rpc = functions.channels.GetMessages(channel=peer, id=ids)
        else:
            rpc = functions.messages.GetMessages(id=ids)

        while True:
            try:
                r = self.send(rpc)
            except FloodWait as e:
                log.warning("Sleeping for {}s".format(e.x))
                time.sleep(e.x)
            else:
                break

        messages = pyrogram.Messages._parse(self, r, replies=replies)

        return messages if is_iterable else messages.messages[0]

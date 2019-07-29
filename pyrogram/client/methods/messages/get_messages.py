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

import asyncio
import logging
from typing import Union, Iterable, List

import pyrogram
from pyrogram.api import functions, types
from pyrogram.errors import FloodWait

from ...ext import BaseClient, utils

log = logging.getLogger(__name__)


# TODO: Rewrite using a flag for replied messages and have message_ids non-optional


class GetMessages(BaseClient):
    async def get_messages(
        self,
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]] = None,
        reply_to_message_ids: Union[int, Iterable[int]] = None,
        replies: int = 1
    ) -> Union["pyrogram.Message", List["pyrogram.Message"]]:
        """Get one or more messages from a chat by using message identifiers.

        You can retrieve up to 200 messages at once.

        Parameters:
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
                The number of subsequent replies to get for each message.
                Pass 0 for no reply at all or -1 for unlimited replies.
                Defaults to 1.

        Returns:
            :obj:`Message` | List of :obj:`Message`: In case *message_ids* was an integer, the single requested message is
            returned, otherwise, in case *message_ids* was an iterable, the returned value will be a list of messages,
            even if such iterable contained just a single element.

        Example:
            .. code-block:: python

                # Get one message
                app.get_messages("pyrogramchat", 51110)

                # Get more than one message (list of messages)
                app.get_messages("pyrogramchat", [44625, 51110])

                # Get message by ignoring any replied-to message
                app.get_messages(chat_id, message_id, replies=0)

                # Get message with all chained replied-to messages
                app.get_messages(chat_id, message_id, replies=-1)

                # Get the replied-to message of a message
                app.get_messages(chat_id, reply_to_message_ids=message_id)

        Raises:
            ValueError: In case of invalid arguments.
        """
        ids, ids_type = (
            (message_ids, types.InputMessageID) if message_ids
            else (reply_to_message_ids, types.InputMessageReplyTo) if reply_to_message_ids
            else (None, None)
        )

        if ids is None:
            raise ValueError("No argument supplied. Either pass message_ids or reply_to_message_ids")

        peer = await self.resolve_peer(chat_id)

        is_iterable = not isinstance(ids, int)
        ids = list(ids) if is_iterable else [ids]
        ids = [ids_type(id=i) for i in ids]

        if replies < 0:
            replies = (1 << 31) - 1

        if isinstance(peer, types.InputPeerChannel):
            rpc = functions.channels.GetMessages(channel=peer, id=ids)
        else:
            rpc = functions.messages.GetMessages(id=ids)

        while True:
            try:
                r = await self.send(rpc)
            except FloodWait as e:
                log.warning("Sleeping for {}s".format(e.x))
                await asyncio.sleep(e.x)
            else:
                break

        messages = await utils.parse_messages(self, r, replies=replies)

        return messages if is_iterable else messages[0]

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

from typing import List

import pyrogram
from pyrogram.api import types
from .message import Message
from ..pyrogram_type import PyrogramType
from ..user_and_chats import Chat


class Messages(PyrogramType):
    """This object represents a chat's messages.

    Args:
        total_count (``int``):
            Total number of messages the target chat has.

        messages (List of :obj:`Message <pyrogram.Message>`):
            Requested messages.
    """

    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 total_count: int,
                 messages: List[Message]):
        super().__init__(client)

        self.total_count = total_count
        self.messages = messages

    @staticmethod
    def _parse(client, messages: types.messages.Messages, replies: int = 1) -> "Messages":
        users = {i.id: i for i in messages.users}
        chats = {i.id: i for i in messages.chats}

        return Messages(
            total_count=getattr(messages, "count", len(messages.messages)),
            messages=[Message._parse(client, message, users, chats, replies) for message in messages.messages],
            client=client
        )

    @staticmethod
    def _parse_deleted(client, update) -> "Messages":
        messages = update.messages
        channel_id = getattr(update, "channel_id", None)

        parsed_messages = []

        for message in messages:
            parsed_messages.append(
                Message(
                    message_id=message,
                    chat=Chat(
                        id=int("-100" + str(channel_id)),
                        type="channel",
                        client=client
                    ) if channel_id is not None else None,
                    client=client
                )
            )

        return Messages(
            total_count=len(parsed_messages),
            messages=parsed_messages,
            client=client
        )

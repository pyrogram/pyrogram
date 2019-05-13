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

from typing import List, Union

import pyrogram
from pyrogram.api import types
from .message import Message
from ..pyrogram_type import PyrogramType
from ..update import Update
from ..user_and_chats import Chat


class Messages(PyrogramType, Update):
    """Contains a chat's messages.

    Parameters:
        total_count (``int``):
            Total number of messages the target chat has.

        messages (List of :obj:`Message`):
            Requested messages.
    """

    __slots__ = ["total_count", "messages"]

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        total_count: int,
        messages: List[Message]
    ):
        super().__init__(client)

        self.total_count = total_count
        self.messages = messages

    @staticmethod
    def _parse(client, messages: types.messages.Messages, replies: int = 1) -> "Messages":
        users = {i.id: i for i in messages.users}
        chats = {i.id: i for i in messages.chats}

        total_count = getattr(messages, "count", len(messages.messages))

        if not messages.messages:
            return Messages(
                total_count=total_count,
                messages=[],
                client=client
            )

        parsed_messages = [Message._parse(client, message, users, chats, replies=0) for message in messages.messages]

        if replies:
            messages_with_replies = {i.id: getattr(i, "reply_to_msg_id", None) for i in messages.messages}
            reply_message_ids = [i[0] for i in filter(lambda x: x[1] is not None, messages_with_replies.items())]

            if reply_message_ids:
                reply_messages = client.get_messages(
                    parsed_messages[0].chat.id,
                    reply_to_message_ids=reply_message_ids,
                    replies=replies - 1
                ).messages

                for message in parsed_messages:
                    reply_id = messages_with_replies[message.message_id]

                    for reply in reply_messages:
                        if reply.message_id == reply_id:
                            message.reply_to_message = reply

        return Messages(
            total_count=total_count,
            messages=parsed_messages,
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

    def forward(
        self,
        chat_id: Union[int, str],
        disable_notification: bool = None,
        as_copy: bool = False,
        remove_caption: bool = False
    ):
        """Bound method *forward* of :obj:`Message`.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            disable_notification (``bool``, *optional*):
                Sends messages silently.
                Users will receive a notification with no sound.

            as_copy (``bool``, *optional*):
                Pass True to forward messages without the forward header (i.e.: send a copy of the message content).
                Defaults to False.

            remove_caption (``bool``, *optional*):
                If set to True and *as_copy* is enabled as well, media captions are not preserved when copying the
                message. Has no effect if *as_copy* is not enabled.
                Defaults to False.

        Returns:
            On success, a :class:`Messages` containing forwarded messages is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        forwarded_messages = []

        for message in self.messages:
            forwarded_messages.append(
                message.forward(
                    chat_id=chat_id,
                    as_copy=as_copy,
                    disable_notification=disable_notification,
                    remove_caption=remove_caption
                )
            )

        return Messages(
            total_count=len(forwarded_messages),
            messages=forwarded_messages,
            client=self._client
        )

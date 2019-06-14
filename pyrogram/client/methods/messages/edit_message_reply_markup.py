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

from typing import Union

import pyrogram
from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient, utils


class EditMessageReplyMarkup(BaseClient):
    def edit_message_reply_markup(
        self,
        reply_markup: "pyrogram.InlineKeyboardMarkup" = None,
        chat_id: Union[int, str] = None,
        message_id: int = None,
        inline_message_id: str = None
    ) -> "pyrogram.Message":
        """Edit only the reply markup of messages sent by the bot or via the bot (for inline bots).

        Parameters:
            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

            chat_id (``int`` | ``str``, *optional*):
                Required if *inline_message_id* is not specified.
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``, *optional*):
                Required if *inline_message_id* is not specified.
                Message identifier in the chat specified in chat_id.

            inline_message_id (``str``, *optional*):
                Required if *chat_id* and *message_id* are not specified.
                Identifier of the inline message.

        Returns:
            :obj:`Message` | ``bool``: On success, if the edited message was sent by the bot, the edited message is
            returned, otherwise True is returned (message sent via the bot, as inline query result).

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        if inline_message_id is not None:
            return self.send(
                functions.messages.EditInlineBotMessage(
                    id=utils.unpack_inline_message_id(inline_message_id),
                    reply_markup=reply_markup.write() if reply_markup else None,
                )
            )

        r = self.send(
            functions.messages.EditMessage(
                peer=self.resolve_peer(chat_id),
                id=message_id,
                reply_markup=reply_markup.write() if reply_markup else None,
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateEditMessage, types.UpdateEditChannelMessage)):
                return pyrogram.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

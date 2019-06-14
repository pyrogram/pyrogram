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
from pyrogram.client.ext import BaseClient


class EditMessageCaption(BaseClient):
    def edit_message_caption(
        self,
        caption: str,
        chat_id: Union[int, str] = None,
        message_id: int = None,
        inline_message_id: str = None,
        parse_mode: str = "",
        reply_markup: "pyrogram.InlineKeyboardMarkup" = None
    ) -> "pyrogram.Message":
        """Edit caption of media messages.

        Parameters:
            caption (``str``):
                New caption of the media message.

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

            parse_mode (``str``, *optional*):
                Pass "markdown" or "html" if you want Telegram apps to show bold, italic, fixed-width text or inline
                URLs in your message. Defaults to "markdown".

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`Message` | ``bool``: On success, if the edited message was sent by the bot, the edited message is
            returned, otherwise True is returned (message sent via the bot, as inline query result).

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        return self.edit_message_text(
            text=caption,
            chat_id=chat_id,
            message_id=message_id,
            inline_message_id=inline_message_id,
            parse_mode=parse_mode,
            reply_markup=reply_markup
        )

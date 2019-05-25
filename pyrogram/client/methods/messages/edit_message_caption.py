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
from pyrogram.client.ext import BaseClient


class EditMessageCaption(BaseClient):
    async def edit_message_caption(
        self,
        chat_id: Union[int, str],
        message_id: int,
        caption: str,
        parse_mode: str = "",
        reply_markup: "pyrogram.InlineKeyboardMarkup" = None
    ) -> "pyrogram.Message":
        """Edit captions of messages.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            caption (``str``):
                New caption of the message.

            parse_mode (``str``, *optional*):
                Pass "markdown" or "html" if you want Telegram apps to show bold, italic, fixed-width text or inline
                URLs in your caption. Defaults to "markdown".

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`Message`: On success, the edited message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown

        r = await self.send(
            functions.messages.EditMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                reply_markup=reply_markup.write() if reply_markup else None,
                **await style.parse(caption)
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateEditMessage, types.UpdateEditChannelMessage)):
                return await pyrogram.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

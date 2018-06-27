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
from pyrogram.client.ext import BaseClient, utils


class EditMessageText(BaseClient):
    def edit_message_text(self,
                          chat_id: int or str,
                          message_id: int,
                          text: str,
                          parse_mode: str = "",
                          disable_web_page_preview: bool = None,
                          reply_markup=None):
        """Use this method to edit text messages.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                For a private channel/supergroup you can use its *t.me/joinchat/* link.

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            text (``str``):
                New text of the message.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your message.
                Defaults to Markdown.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown

        r = self.send(
            functions.messages.EditMessage(
                peer=self.resolve_peer(chat_id),
                id=message_id,
                no_webpage=disable_web_page_preview or None,
                reply_markup=reply_markup.write() if reply_markup else None,
                **style.parse(text)
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateEditMessage, types.UpdateEditChannelMessage)):
                return utils.parse_messages(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

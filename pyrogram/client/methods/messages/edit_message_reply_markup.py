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


class EditMessageReplyMarkup(BaseClient):
    def edit_message_reply_markup(self,
                                  chat_id: int or str,
                                  message_id: int,
                                  reply_markup=None):
        """Use this method to edit only the reply markup of messages sent by the bot or via the bot (for inline bots).

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                For a private channel/supergroup you can use its *t.me/joinchat/* link.

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, if edited message is sent by the bot, the edited
            :obj:`Message <pyrogram.Message>` is returned, otherwise True is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
        """

        r = self.send(
            functions.messages.EditMessage(
                peer=self.resolve_peer(chat_id),
                id=message_id,
                reply_markup=reply_markup.write() if reply_markup else None
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateEditMessage, types.UpdateEditChannelMessage)):
                return utils.parse_messages(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

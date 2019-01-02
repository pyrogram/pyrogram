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
from ...ext import BaseClient


class SendMessage(BaseClient):
    async def send_message(self,
                           chat_id: Union[int, str],
                           text: str,
                           parse_mode: str = "",
                           disable_web_page_preview: bool = None,
                           disable_notification: bool = None,
                           reply_to_message_id: int = None,
                           reply_markup: Union["pyrogram.InlineKeyboardMarkup",
                                               "pyrogram.ReplyKeyboardMarkup",
                                               "pyrogram.ReplyKeyboardRemove",
                                               "pyrogram.ForceReply"] = None) -> "pyrogram.Message":
        """Use this method to send text messages.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            text (``str``):
                Text of the message to be sent.

            parse_mode (``str``, *optional*):
                Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
                if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your message.
                Defaults to Markdown.

            disable_web_page_preview (``bool``, *optional*):
                Disables link previews for links in this message.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``int``, *optional*):
                If the message is a reply, ID of the original message.

            reply_markup (:obj:`InlineKeyboardMarkup` | :obj:`ReplyKeyboardMarkup` | :obj:`ReplyKeyboardRemove` | :obj:`ForceReply`, *optional*):
                Additional interface options. An object for an inline keyboard, custom reply keyboard,
                instructions to remove reply keyboard or to force a reply from the user.

        Returns:
            On success, the sent :obj:`Message` is returned.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """
        style = self.html if parse_mode.lower() == "html" else self.markdown
        message, entities = style.parse(text).values()

        r = await self.send(
            functions.messages.SendMessage(
                peer=await self.resolve_peer(chat_id),
                no_webpage=disable_web_page_preview or None,
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id,
                random_id=self.rnd_id(),
                reply_markup=reply_markup.write() if reply_markup else None,
                message=message,
                entities=entities
            )
        )

        if isinstance(r, types.UpdateShortSentMessage):
            return pyrogram.Message(
                message_id=r.id,
                chat=pyrogram.Chat(
                    id=list((await self.resolve_peer(chat_id)).__dict__.values())[0],
                    type="private",
                    client=self
                ),
                text=message,
                date=r.date,
                outgoing=r.out,
                entities=entities,
                client=self
            )

        for i in r.updates:
            if isinstance(i, (types.UpdateNewMessage, types.UpdateNewChannelMessage)):
                return await pyrogram.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

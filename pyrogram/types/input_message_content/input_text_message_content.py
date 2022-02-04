#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional, List

import pyrogram
from pyrogram import raw, types, utils
from .input_message_content import InputMessageContent


class InputTextMessageContent(InputMessageContent):
    """Content of a text message to be sent as the result of an inline query.

    Parameters:
        message_text (``str``):
            Text of the message to be sent, 1-4096 characters.

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.

        entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in message text, which can be specified instead of *parse_mode*.

        disable_web_page_preview (``bool``, *optional*):
            Disables link previews for links in this message.
    """

    def __init__(
        self,
        message_text: str,
        parse_mode: Optional[str] = object,
        entities: List["types.MessageEntity"] = None,
        disable_web_page_preview: bool = None
    ):
        super().__init__()

        self.message_text = message_text
        self.parse_mode = parse_mode
        self.entities = entities
        self.disable_web_page_preview = disable_web_page_preview

    async def write(self, client: "pyrogram.Client", reply_markup):
        message, entities = (await utils.parse_text_entities(
            client, self.message_text, self.parse_mode, self.entities
        )).values()

        return raw.types.InputBotInlineMessageText(
            no_webpage=self.disable_web_page_preview or None,
            reply_markup=await reply_markup.write(client) if reply_markup else None,
            message=message,
            entities=entities
        )

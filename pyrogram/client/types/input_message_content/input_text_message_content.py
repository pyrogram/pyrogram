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

from typing import Union

from pyrogram.api import types
from .input_message_content import InputMessageContent
from ...parser import Parser


class InputTextMessageContent(InputMessageContent):
    """Content of a text message to be sent as the result of an inline query.

    Parameters:
        message_text (``str``):
            Text of the message to be sent, 1-4096 characters.

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.

        disable_web_page_preview (``bool``, *optional*):
            Disables link previews for links in this message.
    """

    __slots__ = ["message_text", "parse_mode", "disable_web_page_preview"]

    def __init__(self, message_text: str, parse_mode: Union[str, None] = "", disable_web_page_preview: bool = None):
        super().__init__()

        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview

    def write(self, reply_markup):
        return types.InputBotInlineMessageText(
            no_webpage=self.disable_web_page_preview or None,
            reply_markup=reply_markup.write() if reply_markup else None,
            **(Parser(None)).parse(self.message_text, self.parse_mode)
        )

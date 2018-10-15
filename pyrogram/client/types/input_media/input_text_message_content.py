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

from pyrogram.api import types
from pyrogram.client.style import HTML, Markdown


class InputTextMessageContent:
    def __init__(self, message_text: str, parse_mode: str = "", disable_web_page_preview: bool = None):
        self.message_text = message_text
        self.parse_mode = parse_mode
        self.disable_web_page_preview = disable_web_page_preview

        self.style = HTML() if parse_mode.lower() == "html" else Markdown()

    def write(self, reply_markup):
        return types.InputBotInlineMessageText(
            no_webpage=self.disable_web_page_preview or None,
            reply_markup=reply_markup.write(),
            **self.style.parse(self.message_text)
        )

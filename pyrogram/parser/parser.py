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

from collections import OrderedDict
from typing import Optional

import pyrogram
from .html import HTML
from .markdown import Markdown


class Parser:
    def __init__(self, client: Optional["pyrogram.Client"]):
        self.client = client
        self.html = HTML(client)
        self.markdown = Markdown(client)

    async def parse(self, text: str, mode: Optional[str] = object):
        text = str(text if text else "").strip()

        if mode == object:
            if self.client:
                mode = self.client.parse_mode
            else:
                mode = "combined"

        if mode is None:
            return OrderedDict([
                ("message", text),
                ("entities", [])
            ])

        mode = mode.lower()

        if mode == "combined":
            return await self.markdown.parse(text)

        if mode in ["markdown", "md"]:
            return await self.markdown.parse(text, True)

        if mode == "html":
            return await self.html.parse(text)

        raise ValueError('parse_mode must be one of {} or None. Not "{}"'.format(
            ", ".join(f'"{m}"' for m in pyrogram.Client.PARSE_MODES[:-1]),
            mode
        ))

    @staticmethod
    def unparse(text: str, entities: list, is_html: bool):
        if is_html:
            return HTML.unparse(text, entities)
        else:
            return Markdown.unparse(text, entities)

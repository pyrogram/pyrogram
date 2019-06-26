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

from collections import OrderedDict
from typing import Union


import pyrogram
from .html import HTML
from .markdown import Markdown


class Parser:
    def __init__(self, client: Union["pyrogram.BaseClient", None]):
        self.html = HTML(client)
        self.markdown = Markdown(client)

    def parse(self, text: str, mode: str = ""):
        if mode is None:
            return OrderedDict([
                ("message", text),
                ("entities", [])
            ])

        mode = mode.lower()

        if mode == "":
            return self.markdown.parse(text)

        if mode in "markdown":
            return self.markdown.parse(text, True)

        if mode == "html":
            return self.html.parse(text)

    @staticmethod
    def unparse(text: str, entities: list, is_html: bool):
        if is_html:
            return HTML.unparse(text, entities)
        else:
            return Markdown.unparse(text, entities)

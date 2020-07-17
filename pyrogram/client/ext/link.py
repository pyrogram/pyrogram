# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

import html


class Link(str):
    HTML = "<a href={url}>{text}</a>"
    MD = "[{text}]({url})"

    def __init__(self, url: str, text: str, style: str):
        super().__init__()

        self.url = url
        self.text = text
        self.style = style

    @staticmethod
    def format(url: str, text: str, style: str):
        if style in ["md", "markdown"]:
            fmt = Link.MD
        elif style in ["combined", "html", None]:
            fmt = Link.HTML
        else:
            raise ValueError("{} is not a valid style/parse mode".format(style))

        return fmt.format(url=url, text=html.escape(text))

    # noinspection PyArgumentList
    def __new__(cls, url, text, style):
        return str.__new__(cls, Link.format(url, text, style))

    def __call__(self, other: str = None, *, style: str = None):
        return Link.format(self.url, other or self.text, style or self.style)

    def __str__(self):
        return Link.format(self.url, self.text, self.style)

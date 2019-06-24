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

import html
import re

import pyrogram
from .html import HTML


class Markdown:
    BOLD_DELIMITER = "**"
    ITALIC_DELIMITER = "__"
    UNDERLINE_DELIMITER = "--"
    STRIKE_DELIMITER = "~~"
    CODE_DELIMITER = "`"
    PRE_DELIMITER = "```"

    MARKDOWN_RE = re.compile(r"({d})".format(
        d="|".join(
            ["".join(i) for i in [
                [r"\{}".format(j) for j in i]
                for i in [
                    PRE_DELIMITER,
                    CODE_DELIMITER,
                    STRIKE_DELIMITER,
                    UNDERLINE_DELIMITER,
                    ITALIC_DELIMITER,
                    BOLD_DELIMITER
                ]
            ]]
        )))

    URL_RE = re.compile(r"\[([^[]+)]\(([^(]+)\)")

    def __init__(self, client: "pyrogram.BaseClient"):
        self.html = HTML(client)

    def parse(self, text: str):
        offset = 0
        delimiters = set()

        for i, match in enumerate(re.finditer(Markdown.MARKDOWN_RE, text)):
            start, stop = match.span()
            delimiter = match.group(1)

            if delimiter == Markdown.BOLD_DELIMITER:
                tag = "b"
            elif delimiter == Markdown.ITALIC_DELIMITER:
                tag = "i"
            elif delimiter == Markdown.UNDERLINE_DELIMITER:
                tag = "u"
            elif delimiter == Markdown.STRIKE_DELIMITER:
                tag = "s"
            elif delimiter == Markdown.CODE_DELIMITER:
                tag = "code"
            elif delimiter == Markdown.PRE_DELIMITER:
                tag = "pre"
            else:
                continue

            if delimiter not in delimiters:
                delimiters.add(delimiter)
                tag = "<{}>".format(tag)
            else:
                delimiters.remove(delimiter)
                tag = "</{}>".format(tag)

            text = text[:start + offset] + tag + text[stop + offset:]

            offset += len(tag) - len(delimiter)

        offset = 0

        for match in re.finditer(Markdown.URL_RE, text):
            start, stop = match.span()
            full = match.group(0)

            body, url = match.groups()
            body = html.escape(body)

            replace = '<a href="{}">{}</a>'.format(url, body)

            text = text[:start + offset] + replace + text[stop + offset:]

            offset += len(replace) - len(full)

        return self.html.parse(text)

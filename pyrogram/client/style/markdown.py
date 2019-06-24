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
    BOLD_DELIM = "**"
    ITALIC_DELIM = "__"
    UNDERLINE_DELIM = "--"
    STRIKE_DELIM = "~~"
    CODE_DELIM = "`"
    PRE_DELIM = "```"

    MARKDOWN_RE = re.compile(r"({d})".format(
        d="|".join(
            ["".join(i) for i in [
                [r"\{}".format(j) for j in i]
                for i in [
                    PRE_DELIM,
                    CODE_DELIM,
                    STRIKE_DELIM,
                    UNDERLINE_DELIM,
                    ITALIC_DELIM,
                    BOLD_DELIM
                ]
            ]]
        )))

    URL_RE = re.compile(r"\[([^[]+)]\(([^(]+)\)")

    OPENING_TAG = "<{}>"
    CLOSING_TAG = "</{}>"
    URL_MARKUP = '<a href="{}">{}</a>'
    FIXED_WIDTH_DELIMS = [CODE_DELIM, PRE_DELIM]

    def __init__(self, client: "pyrogram.BaseClient"):
        self.html = HTML(client)

    def parse(self, text: str):
        text = html.escape(text)

        offset = 0
        delims = set()

        for i, match in enumerate(re.finditer(Markdown.MARKDOWN_RE, text)):
            start, stop = match.span()
            delim = match.group(1)

            if delim == Markdown.BOLD_DELIM:
                tag = "b"
            elif delim == Markdown.ITALIC_DELIM:
                tag = "i"
            elif delim == Markdown.UNDERLINE_DELIM:
                tag = "u"
            elif delim == Markdown.STRIKE_DELIM:
                tag = "s"
            elif delim == Markdown.CODE_DELIM:
                tag = "code"
            elif delim == Markdown.PRE_DELIM:
                tag = "pre"
            else:
                continue

            if delim not in Markdown.FIXED_WIDTH_DELIMS and any(x in delims for x in Markdown.FIXED_WIDTH_DELIMS):
                continue

            if delim not in delims:
                delims.add(delim)
                tag = Markdown.OPENING_TAG.format(tag)
            else:
                delims.remove(delim)
                tag = Markdown.CLOSING_TAG.format(tag)

            text = text[:start + offset] + tag + text[stop + offset:]

            offset += len(tag) - len(delim)

        offset = 0

        for match in re.finditer(Markdown.URL_RE, text):
            start, stop = match.span()
            full = match.group(0)

            body, url = match.groups()
            replace = Markdown.URL_MARKUP.format(url, body)

            text = text[:start + offset] + replace + text[stop + offset:]

            offset += len(replace) - len(full)

        return self.html.parse(text)

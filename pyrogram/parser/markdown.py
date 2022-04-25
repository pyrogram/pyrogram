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

import html
import re
from typing import Optional

import pyrogram
from pyrogram.enums import MessageEntityType
from . import utils
from .html import HTML

BOLD_DELIM = "**"
ITALIC_DELIM = "__"
UNDERLINE_DELIM = "--"
STRIKE_DELIM = "~~"
SPOILER_DELIM = "||"
CODE_DELIM = "`"
PRE_DELIM = "```"

MARKDOWN_RE = re.compile(r"({d})|\[(.+?)\]\((.+?)\)".format(
    d="|".join(
        ["".join(i) for i in [
            [rf"\{j}" for j in i]
            for i in [
                PRE_DELIM,
                CODE_DELIM,
                STRIKE_DELIM,
                UNDERLINE_DELIM,
                ITALIC_DELIM,
                BOLD_DELIM,
                SPOILER_DELIM
            ]
        ]]
    )))

OPENING_TAG = "<{}>"
CLOSING_TAG = "</{}>"
URL_MARKUP = '<a href="{}">{}</a>'
FIXED_WIDTH_DELIMS = [CODE_DELIM, PRE_DELIM]


class Markdown:
    def __init__(self, client: Optional["pyrogram.Client"]):
        self.html = HTML(client)

    async def parse(self, text: str, strict: bool = False):
        if strict:
            text = html.escape(text)

        delims = set()
        is_fixed_width = False

        for i, match in enumerate(re.finditer(MARKDOWN_RE, text)):
            start, _ = match.span()
            delim, text_url, url = match.groups()
            full = match.group(0)

            if delim in FIXED_WIDTH_DELIMS:
                is_fixed_width = not is_fixed_width

            if is_fixed_width and delim not in FIXED_WIDTH_DELIMS:
                continue

            if text_url:
                text = utils.replace_once(text, full, URL_MARKUP.format(url, text_url), start)
                continue

            if delim == BOLD_DELIM:
                tag = "b"
            elif delim == ITALIC_DELIM:
                tag = "i"
            elif delim == UNDERLINE_DELIM:
                tag = "u"
            elif delim == STRIKE_DELIM:
                tag = "s"
            elif delim == CODE_DELIM:
                tag = "code"
            elif delim == PRE_DELIM:
                tag = "pre"
            elif delim == SPOILER_DELIM:
                tag = "spoiler"
            else:
                continue

            if delim not in delims:
                delims.add(delim)
                tag = OPENING_TAG.format(tag)
            else:
                delims.remove(delim)
                tag = CLOSING_TAG.format(tag)

            text = utils.replace_once(text, delim, tag, start)

        return await self.html.parse(text)

    @staticmethod
    def unparse(text: str, entities: list):
        text = utils.add_surrogates(text)

        entities_offsets = []

        for entity in entities:
            entity_type = entity.type
            start = entity.offset
            end = start + entity.length

            if entity_type == MessageEntityType.BOLD:
                start_tag = end_tag = BOLD_DELIM
            elif entity_type == MessageEntityType.ITALIC:
                start_tag = end_tag = ITALIC_DELIM
            elif entity_type == MessageEntityType.UNDERLINE:
                start_tag = end_tag = UNDERLINE_DELIM
            elif entity_type == MessageEntityType.STRIKETHROUGH:
                start_tag = end_tag = STRIKE_DELIM
            elif entity_type == MessageEntityType.CODE:
                start_tag = end_tag = CODE_DELIM
            elif entity_type in (MessageEntityType.PRE, MessageEntityType.BLOCKQUOTE):
                start_tag = end_tag = PRE_DELIM
            elif entity_type == MessageEntityType.SPOILER:
                start_tag = end_tag = SPOILER_DELIM
            elif entity_type == MessageEntityType.TEXT_LINK:
                url = entity.url
                start_tag = "["
                end_tag = f"]({url})"
            elif entity_type == MessageEntityType.TEXT_MENTION:
                user = entity.user
                start_tag = "["
                end_tag = f"](tg://user?id={user.id})"
            else:
                continue

            entities_offsets.append((start_tag, start,))
            entities_offsets.append((end_tag, end,))

        entities_offsets = map(
            lambda x: x[1],
            sorted(
                enumerate(entities_offsets),
                key=lambda x: (x[1][1], x[0]),
                reverse=True
            )
        )

        for entity, offset in entities_offsets:
            text = text[:offset] + entity + text[offset:]

        return utils.remove_surrogates(text)

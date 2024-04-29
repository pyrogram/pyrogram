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
BLOCKQUOTE_DELIM = ">"

MARKDOWN_RE = re.compile(r"({d})|(!?)\[(.+?)\]\((.+?)\)".format(
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
EMOJI_MARKUP = '<emoji id={}>{}</emoji>'
FIXED_WIDTH_DELIMS = [CODE_DELIM, PRE_DELIM]


class Markdown:
    def __init__(self, client: Optional["pyrogram.Client"]):
        self.html = HTML(client)

    def _parse_blockquotes(self, text: str):
        text = html.unescape(text)
        lines = text.split('\n')
        result = []
        in_blockquote = False
        current_blockquote = []

        for line in lines:
            if line.startswith(BLOCKQUOTE_DELIM):
                in_blockquote = True
                current_blockquote.append(line[1:].strip())
            else:
                if in_blockquote:
                    in_blockquote = False
                    result.append(OPENING_TAG.format("blockquote") + '\n'.join(current_blockquote) + CLOSING_TAG.format("blockquote"))
                    current_blockquote = []
                result.append(line)

        if in_blockquote:
            result.append(OPENING_TAG.format("blockquote") + '\n'.join(current_blockquote) + CLOSING_TAG.format("blockquote"))

        return '\n'.join(result)

    async def parse(self, text: str, strict: bool = False):
        if strict:
            text = html.escape(text)

        text = self._parse_blockquotes(text)

        delims = set()
        is_fixed_width = False

        for i, match in enumerate(re.finditer(MARKDOWN_RE, text)):
            start, _ = match.span()
            delim, is_emoji, text_url, url = match.groups()
            full = match.group(0)

            if delim in FIXED_WIDTH_DELIMS:
                is_fixed_width = not is_fixed_width

            if is_fixed_width and delim not in FIXED_WIDTH_DELIMS:
                continue

            if not is_emoji and text_url:
                text = utils.replace_once(text, full, URL_MARKUP.format(url, text_url), start)
                continue

            if is_emoji:
                emoji = text_url
                emoji_id = url.lstrip("tg://emoji?id=")
                text = utils.replace_once(text, full, EMOJI_MARKUP.format(emoji_id, emoji), start)
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

            if delim == PRE_DELIM and delim in delims:
                delim_and_language = text[text.find(PRE_DELIM):].split("\n")[0]
                language = delim_and_language[len(PRE_DELIM):]
                text = utils.replace_once(text, delim_and_language, f'<pre language="{language}">', start)
                continue

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
            elif entity_type == MessageEntityType.PRE:
                language = getattr(entity, "language", "") or ""
                start_tag = f"{PRE_DELIM}{language}\n"
                end_tag = f"\n{PRE_DELIM}"
            elif entity_type == MessageEntityType.BLOCKQUOTE:
                start_tag = BLOCKQUOTE_DELIM + " "
                end_tag = ""
                blockquote_text = text[start:end]
                lines = blockquote_text.split("\n")
                last_length = 0
                for line in lines:
                    if len(line) == 0 and last_length == end:
                        continue
                    start_offset = start+last_length
                    last_length = last_length+len(line)
                    end_offset = start_offset+last_length
                    entities_offsets.append((start_tag, start_offset,))
                    entities_offsets.append((end_tag, end_offset,))
                    last_length = last_length+1
                continue
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
            elif entity_type == MessageEntityType.CUSTOM_EMOJI:
                emoji_id = entity.custom_emoji_id
                start_tag = "!["
                end_tag = f"](tg://emoji?id={emoji_id})"
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

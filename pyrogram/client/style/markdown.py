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

import re

from pyrogram.api.types import (
    MessageEntityBold as Bold,
    MessageEntityItalic as Italic,
    MessageEntityCode as Code,
    MessageEntityTextUrl as Url,
    MessageEntityPre as Pre,
    MessageEntityMentionName as MentionInvalid,
    InputMessageEntityMentionName as Mention
)
from . import utils


class Markdown:
    BOLD_DELIMITER = "**"
    ITALIC_DELIMITER = "__"
    CODE_DELIMITER = "`"
    PRE_DELIMITER = "```"

    MARKDOWN_RE = re.compile(r"```([\w ]*)\n([\w\W]*)(?:\n|)```|\[([^[(]+)\]\(([^])]+)\)|({d})(.+?)\5".format(
        d="|".join(
            ["".join(i) for i in [
                ["\{}".format(j) for j in i]
                for i in [
                    PRE_DELIMITER,
                    CODE_DELIMITER,
                    ITALIC_DELIMITER,
                    BOLD_DELIMITER
                ]
            ]]
        )
    ))
    MENTION_RE = re.compile(r"tg://user\?id=(\d+)")

    def __init__(self, peers_by_id: dict):
        self.peers_by_id = peers_by_id

    def parse(self, message: str):
        entities = []
        message = utils.add_surrogates(message).strip()
        offset = 0

        for match in self.MARKDOWN_RE.finditer(message):
            start = match.start() - offset
            lang, pre, text, url, style, body = match.groups()

            if pre:
                body = pre = pre.strip()
                entity = Pre(start, len(pre), lang.strip() or "")
                offset += len(lang) + len(self.PRE_DELIMITER) * 2
            elif url:
                mention = self.MENTION_RE.match(url)

                if mention:
                    user_id = int(mention.group(1))
                    input_user = self.peers_by_id.get(user_id, None)

                    entity = (
                        Mention(start, len(text), input_user)
                        if input_user
                        else MentionInvalid(start, len(text), user_id)
                    )
                else:
                    entity = Url(start, len(text), url)

                body = text
                offset += len(url) + 4
            else:
                if style == self.BOLD_DELIMITER:
                    entity = Bold(start, len(body))
                elif style == self.ITALIC_DELIMITER:
                    entity = Italic(start, len(body))
                elif style == self.CODE_DELIMITER:
                    entity = Code(start, len(body))
                elif style == self.PRE_DELIMITER:
                    entity = Pre(start, len(body), "")
                else:
                    continue

                offset += len(style) * 2

            entities.append(entity)
            message = message.replace(match.group(), body)

        return dict(
            message=utils.remove_surrogates(message),
            entities=entities
        )

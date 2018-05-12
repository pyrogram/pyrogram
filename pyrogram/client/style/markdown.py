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

    MARKDOWN_RE = re.compile(r"({d})([\w\W]*?)\1|\[([^[]+?)\]\(([^(]+?)\)".format(
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
        message = utils.add_surrogates(message).strip()
        entities = []
        offset = 0

        for match in self.MARKDOWN_RE.finditer(message):
            start = match.start() - offset
            style, body, text, url = match.groups()

            if url:
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

    def unparse(self, message: str, entities: list):
        message = utils.add_surrogates(message).strip()
        offset = 0

        for entity in entities:
            start = entity.offset + offset
            type = entity.type
            url = entity.url
            user = entity.user
            sub = message[start: start + entity.length]

            if type == "bold":
                style = self.BOLD_DELIMITER
            elif type == "italic":
                style = self.ITALIC_DELIMITER
            elif type == "code":
                style = self.CODE_DELIMITER
            elif type == "pre":
                style = self.PRE_DELIMITER
            elif type == "text_link":
                offset += 4 + len(url)
                message = message[:start] + message[start:].replace(
                    sub, "[{}]({})".format(sub, url), 1)
                continue
            elif type == "text_mention":
                offset += 17 + len(str(user.id))
                message = message[:start] + message[start:].replace(
                    sub, "[{}](tg://user?id={})".format(sub, user.id), 1)
                continue
            else:
                continue

            offset += len(style) * 2
            message = message[:start] + message[start:].replace(
                sub, "{0}{1}{0}".format(style, sub), 1)

        return utils.remove_surrogates(message)

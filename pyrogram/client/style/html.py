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
    InputMessageEntityMentionName as Mention,
)
from . import utils


class HTML:
    HTML_RE = re.compile(r"<(\w+)(?: href=([\"'])([^<]+)\2)?>([^>]+)</\1>")
    MENTION_RE = re.compile(r"tg://user\?id=(\d+)")

    def __init__(self, peers_by_id):
        self.peers_by_id = peers_by_id

    def parse(self, text):
        entities = []
        text = utils.add_surrogates(text)
        offset = 0

        for match in self.HTML_RE.finditer(text):
            start = match.start() - offset
            style, url, body = match.group(1, 3, 4)

            if url:
                mention = self.MENTION_RE.match(url)

                if mention:
                    user_id = int(mention.group(1))
                    input_user = self.peers_by_id.get(user_id, None)

                    entity = (
                        Mention(start, len(body), input_user)
                        if input_user else MentionInvalid(start, len(body), user_id)
                    )
                else:
                    entity = Url(start, len(body), url)
            else:
                if style == "b" or style == "strong":
                    entity = Bold(start, len(body))
                elif style == "i" or style == "em":
                    entity = Italic(start, len(body))
                elif style == "code":
                    entity = Code(start, len(body))
                elif style == "pre":
                    entity = Pre(start, len(body), "")
                else:
                    continue

            entities.append(entity)
            text = text.replace(match.group(), body)
            offset += len(style) * 2 + 5 + (len(url) + 8 if url else 0)

        return dict(
            message=utils.remove_surrogates(text),
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
                style = "b"
            elif type == "italic":
                style = "i"
            elif type == "code":
                style = "code"
            elif type == "pre":
                style = "pre"
            elif type == "text_link":
                offset += 15 + len(url)
                message = message[:start] + message[start:].replace(
                    sub, "<a href=\"{}\">{}</a>".format(url, sub), 1)
                continue
            elif type == "text_mention":
                offset += 28 + len(str(user.id))
                message = message[:start] + message[start:].replace(
                    sub, "<a href=\"tg://user?id={}\">{}</a>".format(user.id, sub), 1)
                continue
            else:
                continue

            offset += len(style) * 2 + 5
            message = message[:start] + message[start:].replace(
                sub, "<{0}>{1}</{0}>".format(style, sub), 1)

        return utils.remove_surrogates(message)

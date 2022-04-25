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
import logging
import re
from html.parser import HTMLParser
from typing import Optional

import pyrogram
from pyrogram import raw
from pyrogram.enums import MessageEntityType
from pyrogram.errors import PeerIdInvalid
from . import utils

log = logging.getLogger(__name__)


class Parser(HTMLParser):
    MENTION_RE = re.compile(r"tg://user\?id=(\d+)")

    def __init__(self, client: "pyrogram.Client"):
        super().__init__()

        self.client = client

        self.text = ""
        self.entities = []
        self.tag_entities = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        extra = {}

        if tag in ["b", "strong"]:
            entity = raw.types.MessageEntityBold
        elif tag in ["i", "em"]:
            entity = raw.types.MessageEntityItalic
        elif tag == "u":
            entity = raw.types.MessageEntityUnderline
        elif tag in ["s", "del", "strike"]:
            entity = raw.types.MessageEntityStrike
        elif tag == "blockquote":
            entity = raw.types.MessageEntityBlockquote
        elif tag == "code":
            entity = raw.types.MessageEntityCode
        elif tag == "pre":
            entity = raw.types.MessageEntityPre
            extra["language"] = ""
        elif tag == "spoiler":
            entity = raw.types.MessageEntitySpoiler
        elif tag == "a":
            url = attrs.get("href", "")

            mention = Parser.MENTION_RE.match(url)

            if mention:
                entity = raw.types.InputMessageEntityMentionName
                extra["user_id"] = int(mention.group(1))
            else:
                entity = raw.types.MessageEntityTextUrl
                extra["url"] = url
        else:
            return

        if tag not in self.tag_entities:
            self.tag_entities[tag] = []

        self.tag_entities[tag].append(entity(offset=len(self.text), length=0, **extra))

    def handle_data(self, data):
        data = html.unescape(data)

        for entities in self.tag_entities.values():
            for entity in entities:
                entity.length += len(data)

        self.text += data

    def handle_endtag(self, tag):
        try:
            self.entities.append(self.tag_entities[tag].pop())
        except (KeyError, IndexError):
            line, offset = self.getpos()
            offset += 1

            log.debug(f"Unmatched closing tag </{tag}> at line {line}:{offset}")
        else:
            if not self.tag_entities[tag]:
                self.tag_entities.pop(tag)

    def error(self, message):
        pass


class HTML:
    def __init__(self, client: Optional["pyrogram.Client"]):
        self.client = client

    async def parse(self, text: str):
        # Strip whitespace characters from the end of the message, but preserve closing tags
        text = re.sub(r"\s*(</[\w</>]*>)\s*$", r"\1", text)

        parser = Parser(self.client)
        parser.feed(utils.add_surrogates(text))
        parser.close()

        if parser.tag_entities:
            unclosed_tags = []

            for tag, entities in parser.tag_entities.items():
                unclosed_tags.append(f"<{tag}> (x{len(entities)})")

            log.warning(f"Unclosed tags: {', '.join(unclosed_tags)}")

        entities = []

        for entity in parser.entities:
            if isinstance(entity, raw.types.InputMessageEntityMentionName):
                try:
                    if self.client is not None:
                        entity.user_id = await self.client.resolve_peer(entity.user_id)
                except PeerIdInvalid:
                    continue

            entities.append(entity)

        return {
            "message": utils.remove_surrogates(parser.text),
            "entities": sorted(entities, key=lambda e: e.offset)
        }

    @staticmethod
    def unparse(text: str, entities: list):
        text = utils.add_surrogates(text)

        entities_offsets = []

        for entity in entities:
            entity_type = entity.type
            start = entity.offset
            end = start + entity.length

            if entity_type in (MessageEntityType.BOLD, MessageEntityType.ITALIC, MessageEntityType.UNDERLINE,
                               MessageEntityType.STRIKETHROUGH):
                name = entity_type.name[0].lower()
                start_tag = f"<{name}>"
                end_tag = f"</{name}>"
            elif entity_type in (MessageEntityType.CODE, MessageEntityType.PRE, MessageEntityType.BLOCKQUOTE,
                                 MessageEntityType.SPOILER):
                name = entity_type.name.lower()
                start_tag = f"<{name}>"
                end_tag = f"</{name}>"
            elif entity_type == MessageEntityType.TEXT_LINK:
                url = entity.url
                start_tag = f'<a href="{url}">'
                end_tag = "</a>"
            elif entity_type == MessageEntityType.TEXT_MENTION:
                user = entity.user
                start_tag = f'<a href="tg://user?id={user.id}">'
                end_tag = "</a>"
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

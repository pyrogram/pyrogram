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
from collections import OrderedDict
from html.parser import HTMLParser

import pyrogram
from pyrogram.api import types
from pyrogram.errors import PeerIdInvalid
from . import utils


class Parser(HTMLParser):
    MENTION_RE = re.compile(r"tg://user\?id=(\d+)")

    def __init__(self, client: "pyrogram.BaseClient"):
        super().__init__()

        self.client = client

        self.text = ""
        self.entities = []
        self.temp_entities = []
        self.tags = []

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        extra = {}

        if tag in ["b", "strong"]:
            entity = types.MessageEntityBold
        elif tag in ["i", "em"]:
            entity = types.MessageEntityItalic
        elif tag == "u":
            entity = types.MessageEntityUnderline
        elif tag in ["s", "del", "strike"]:
            entity = types.MessageEntityStrike
        elif tag == "blockquote":
            entity = types.MessageEntityBlockquote
        elif tag == "code":
            entity = types.MessageEntityCode
        elif tag == "pre":
            entity = types.MessageEntityPre
            extra["language"] = ""
        elif tag == "a":
            url = attrs.get("href", "")

            mention = Parser.MENTION_RE.match(url)

            if mention:
                user_id = int(mention.group(1))

                try:
                    user = self.client.resolve_peer(user_id)
                except PeerIdInvalid:
                    entity = types.MessageEntityMentionName
                    extra["user_id"] = user_id
                else:
                    entity = types.InputMessageEntityMentionName
                    extra["user_id"] = user
            else:
                entity = types.MessageEntityTextUrl
                extra["url"] = url
        else:
            return

        self.tags.append(tag)
        self.temp_entities.append(entity(offset=len(self.text), length=0, **extra))

    def handle_data(self, data):
        data = html.unescape(data)

        for entity in self.temp_entities:
            entity.length += len(data)

        self.text += data

    def handle_endtag(self, tag):
        start_tag = self.tags.pop()

        if start_tag != tag:
            line, offset = self.getpos()
            offset += 1

            raise ValueError("Expected end tag </{}>, but found </{}> at {}:{}".format(start_tag, tag, line, offset))

        self.entities.append(self.temp_entities.pop())

    def error(self, message):
        pass


class HTML:
    def __init__(self, client: "pyrogram.BaseClient" = None):
        self.client = client

    def parse(self, text: str):
        text = utils.add_surrogates(str(text or "").strip())

        parser = Parser(self.client)
        parser.feed(text)
        print(parser.entities)

        # TODO: OrderedDict to be removed in Python 3.6
        return OrderedDict([
            ("message", utils.remove_surrogates(parser.text)),
            ("entities", parser.entities)
        ])

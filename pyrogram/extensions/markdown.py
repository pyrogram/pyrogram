# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017 Dan Tès <https://github.com/delivrance>
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
from struct import unpack

from pyrogram.api.types import (
    MessageEntityBold as Bold,
    MessageEntityItalic as Italic,
    MessageEntityCode as Code,
    MessageEntityTextUrl as Url,
    MessageEntityPre as Pre,
    InputMessageEntityMentionName as Mention
)


class Markdown:
    INLINE_DELIMITERS = {
        "**": Bold,
        "__": Italic,
        "`": Code
    }

    # SMP = Supplementary Multilingual Plane: https://en.wikipedia.org/wiki/Plane_(Unicode)#Overview
    SMP_RE = re.compile(r"[\U00010000-\U0010FFFF]")

    # ``` python
    # for i in range(10):
    #     print(i)
    # ```
    PRE_RE = r"(?P<pre>```(?P<lang>.*)\n(?P<code>(.|\n)*)\n```)"

    # [url](github.com)
    URL_RE = r"(?P<url>(\[(?P<url_text>.+?)\]\((?P<url_path>.+?)\)))"

    # [name](tg://user?id=123456789)
    MENTION_RE = r"(?P<mention>(\[(?P<mention_text>.+?)\]\(tg:\/\/user\?id=(?P<user_id>\d+?)\)))"

    # **bold**
    # __italic__
    # `code`
    INLINE_RE = r"(?P<inline>(?P<start_delimiter>{d})(?P<body>.+?)(?P<end_delimiter>{d}))".format(
        d="|".join(
            ["".join(i) for i in [
                ["\{}".format(j) for j in i]
                for i in sorted(  # Sort delimiters by length
                    INLINE_DELIMITERS.keys(),
                    key=lambda k: len(k),  # Or: key=len
                    reverse=True
                )
            ]]
        )
    )

    MARKDOWN_RE = re.compile("|".join([PRE_RE, MENTION_RE, URL_RE, INLINE_RE]))

    @classmethod
    def add_surrogates(cls, text):
        # Replace each SMP code point with a surrogate pair
        return cls.SMP_RE.sub(
            lambda match:  # Split SMP in two surrogates
            "".join(chr(i) for i in unpack("<HH", match.group().encode("utf-16le")))
            , text
        )

    @staticmethod
    def remove_surrogates(text):
        # Replace each surrogate pair with a SMP code point
        return text.encode("utf-16", "surrogatepass").decode("utf-16")

    def __init__(self, peers_by_id):
        self.peers_by_id = peers_by_id

    def parse(self, text):
        entities = []
        text = self.add_surrogates(text)
        offset = 0

        for match in self.MARKDOWN_RE.finditer(text):
            start = match.start() - offset

            if match.group("pre"):
                pattern = match.group("pre")
                lang = match.group("lang")
                replace = match.group("code")
                entity = Pre(start, len(replace), lang.strip())
                offset += len(lang) + 8
            elif match.group("url"):
                pattern = match.group("url")
                replace = match.group("url_text")
                path = match.group("url_path")
                entity = Url(start, len(replace), path)
                offset += len(path) + 4
            elif match.group("mention"):
                pattern = match.group("mention")
                replace = match.group("mention_text")
                user_id = match.group("user_id")
                entity = Mention(start, len(replace), self.peers_by_id[int(user_id)])
                offset += len(user_id) + 17
            elif match.group("inline"):
                pattern = match.group("inline")
                replace = match.group("body")
                start_delimiter = match.group("start_delimiter")
                end_delimiter = match.group("end_delimiter")

                if start_delimiter != end_delimiter:
                    continue

                entity = self.INLINE_DELIMITERS[start_delimiter](start, len(replace))
                offset += len(start_delimiter) * 2
            else:
                continue

            entities.append(entity)
            text = text.replace(pattern, replace)

        return dict(
            message=self.remove_surrogates(text),
            entities=entities
        )

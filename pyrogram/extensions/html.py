import re
from struct import unpack

from pyrogram.api.types import (
    MessageEntityBold as Bold,
    MessageEntityItalic as Italic,
    MessageEntityCode as Code,
    MessageEntityTextUrl as Url,
    MessageEntityPre as Pre,
    MessageEntityMentionName as MentionInvalid,
    InputMessageEntityMentionName as Mention,
)


class HTML:
    SMP_RE = re.compile(r"[\U00010000-\U0010FFFF]")
    HTML_RE = re.compile(r"<(\w+)(?: href=\"(.*)\")?>(.*)</\1>")
    MENTION_RE = re.compile(r"tg://user\?id=(\d+)")

    @classmethod
    def add_surrogates(cls, text):
        return cls.SMP_RE.sub(
            lambda match:  # Split SMP in two surrogates
            "".join(chr(i) for i in unpack("<HH", match.group().encode("utf-16le"))),
            text
        )

    @staticmethod
    def remove_surrogates(text):
        return text.encode("utf-16", "surrogatepass").decode("utf-16")

    def __init__(self, peers_by_id):
        self.peers_by_id = peers_by_id

    def parse(self, text):
        entities = []
        text = self.add_surrogates(text)
        offset = 0

        for match in self.HTML_RE.finditer(text):
            start = match.start() - offset
            style, url, body = match.groups()

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
            message=self.remove_surrogates(text),
            entities=entities
        )

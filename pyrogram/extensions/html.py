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


class HTML:
    SMP_RE = re.compile(r"[\U00010000-\U0010FFFF]")

    BOLD_RE = r"(?P<b><b>(?P<b_body>.*?)</b>)"
    STRONG_RE = r"(?P<strong><strong>(?P<strong_body>.*?)</strong>)"
    ITALIC_RE = r"(?P<i><i>(?P<i_body>.*?)</i>)"
    EMPATHIZE_RE = r"(?P<em><em>(?P<em_body>.*?)</em>)"
    CODE_RE = r"(?P<code><code>(?P<code_body>.*?)</code>)"
    PRE_RE = r"(?P<pre><pre>(?P<pre_body>.*?)</pre>)"
    MENTION_RE = r"(?P<mention><a href=\"tg://user\?id=(?P<user_id>\d+?)\">(?P<mention_text>.*?)</a>)"
    URL_RE = r"(?P<url><a href=\"(?P<url_path>.*?)\">(?P<url_text>.*?)</a>)"

    HTML_RE = re.compile("|".join([BOLD_RE, STRONG_RE, ITALIC_RE, EMPATHIZE_RE, CODE_RE, PRE_RE, MENTION_RE, URL_RE]))

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

        # TODO: Beautify ifs
        for match in self.HTML_RE.finditer(text):
            start = match.start() - offset

            if match.group("b"):
                pattern = match.group("b")
                body = match.group("b_body")
                entity = Bold(start, len(body))
                offset += 7
            elif match.group("strong"):
                pattern = match.group("strong")
                body = match.group("strong_body")
                entity = Bold(start, len(body))
                offset += 17
            elif match.group("i"):
                pattern = match.group("i")
                body = match.group("i_body")
                entity = Italic(start, len(body))
                offset += 7
            elif match.group("em"):
                pattern = match.group("em")
                body = match.group("em_body")
                entity = Italic(start, len(body))
                offset += 9
            elif match.group("code"):
                pattern = match.group("code")
                body = match.group("code_body")
                entity = Code(start, len(body))
                offset += 13
            elif match.group("pre"):
                pattern = match.group("pre")
                body = match.group("pre_body")
                entity = Pre(start, len(body), "")
                offset += 11
            elif match.group("mention"):
                pattern = match.group("mention")
                body = match.group("mention_text")
                user_id = match.group("user_id")
                entity = Mention(start, len(body), self.peers_by_id[int(user_id)])
                offset += len(user_id) + 28
            elif match.group("url"):
                pattern = match.group("url")
                body = match.group("url_text")
                path = match.group("url_path")
                entity = Url(start, len(body), path)
                offset += len(path) + 15
            else:
                continue

            entities.append(entity)
            text = text.replace(pattern, body)

        return dict(
            message=self.remove_surrogates(text),
            entities=entities
        )

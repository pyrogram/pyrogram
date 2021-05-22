#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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

from enum import Enum, auto
from typing import Optional

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class AutoName(Enum):
    def _generate_next_value_(self, *args):
        return self.lower()


class MessageEntityType(AutoName):
    MENTION = auto()
    HASHTAG = auto()
    CASHTAG = auto()
    BOT_COMMAND = auto()
    URL = auto()
    EMAIL = auto()
    PHONE_NUMBER = auto()
    BOLD = auto()
    ITALIC = auto()
    UNDERLINE = auto()
    STRIKETHROUGH = auto()
    CODE = auto()
    PRE = auto()
    TEXT_LINK = auto()
    TEXT_MENTION = auto()
    BLOCKQUOTE = auto()


RAW_ENTITIES_TO_TYPE = {
    raw.types.MessageEntityMention: MessageEntityType.MENTION,
    raw.types.MessageEntityHashtag: MessageEntityType.HASHTAG,
    raw.types.MessageEntityCashtag: MessageEntityType.CASHTAG,
    raw.types.MessageEntityBotCommand: MessageEntityType.BOT_COMMAND,
    raw.types.MessageEntityUrl: MessageEntityType.URL,
    raw.types.MessageEntityEmail: MessageEntityType.EMAIL,
    raw.types.MessageEntityBold: MessageEntityType.BOLD,
    raw.types.MessageEntityItalic: MessageEntityType.ITALIC,
    raw.types.MessageEntityCode: MessageEntityType.CODE,
    raw.types.MessageEntityPre: MessageEntityType.PRE,
    raw.types.MessageEntityUnderline: MessageEntityType.UNDERLINE,
    raw.types.MessageEntityStrike: MessageEntityType.STRIKETHROUGH,
    raw.types.MessageEntityBlockquote: MessageEntityType.BLOCKQUOTE,
    raw.types.MessageEntityTextUrl: MessageEntityType.TEXT_LINK,
    raw.types.MessageEntityMentionName: MessageEntityType.TEXT_MENTION,
    raw.types.MessageEntityPhone: MessageEntityType.PHONE_NUMBER
}

TYPE_TO_RAW_ENTITIES = {v.value: k for k, v in RAW_ENTITIES_TO_TYPE.items()}


class MessageEntity(Object):
    """One special entity in a text message.
    For example, hashtags, usernames, URLs, etc.

    Parameters:
        type (``str``):
            Type of the entity. Can be:

            - "mention": ``@username``.
            - "hashtag": ``#hashtag``.
            - "cashtag": ``$PYRO``.
            - "bot_command": ``/start@pyrogrambot``.
            - "url": ``https://pyrogram.org`` (see *url* below).
            - "email": ``do-not-reply@pyrogram.org``.
            - "phone_number": ``+69-420-1337``.
            - "bold": **bold text**.
            - "italic": *italic text*.
            - "underline": underlined text.
            - "strikethrough": strikethrough text.
            - "code": monowidth string.
            - "pre": monowidth block (see *language* below).
            - "text_link": for clickable text URLs.
            - "text_mention": for users without usernames (see *user* below).

        offset (``int``):
            Offset in UTF-16 code units to the start of the entity.

        length (``int``):
            Length of the entity in UTF-16 code units.

        url (``str``, *optional*):
            For "text_link" only, url that will be opened after user taps on the text.

        user (:obj:`~pyrogram.types.User`, *optional*):
            For "text_mention" only, the mentioned user.

        language (``str``. *optional*):
            For "pre" only, the programming language of the entity text.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        type: str,
        offset: int,
        length: int,
        url: str = None,
        user: "types.User" = None,
        language: str = None
    ):
        super().__init__(client)

        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user
        self.language = language

    @staticmethod
    def _parse(client, entity, users: dict) -> Optional["MessageEntity"]:
        type = RAW_ENTITIES_TO_TYPE.get(entity.__class__, None)

        if type is None:
            return None

        return MessageEntity(
            type=type.value,
            offset=entity.offset,
            length=entity.length,
            url=getattr(entity, "url", None),
            user=types.User._parse(client, users.get(getattr(entity, "user_id", None), None)),
            language=getattr(entity, "language", None),
            client=client
        )

    async def write(self):
        args = self.__dict__.copy()

        for arg in ("_client", "type", "user"):
            args.pop(arg)

        if self.user:
            args["user_id"] = await self._client.resolve_peer(self.user.id)

        if not self.url:
            args.pop("url")

        if self.language is None:
            args.pop("language")

        try:
            entity = TYPE_TO_RAW_ENTITIES[self.type]

            if entity is raw.types.MessageEntityMentionName:
                entity = raw.types.InputMessageEntityMentionName
        except KeyError as e:
            raise ValueError(f"Invalid message entity type {e}")
        else:
            try:
                return entity(**args)
            except TypeError as e:
                raise TypeError(f"{entity.QUALNAME}'s {e}")

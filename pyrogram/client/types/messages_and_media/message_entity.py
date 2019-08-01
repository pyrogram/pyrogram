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

import pyrogram

from pyrogram.api import types
from ..object import Object
from ..user_and_chats.user import User


class MessageEntity(Object):
    """One special entity in a text message.
    For example, hashtags, usernames, URLs, etc.

    Parameters:
        type (``str``):
            Type of the entity.
            Can be "mention" (@username), "hashtag", "cashtag", "bot_command", "url", "email", "phone_number", "bold"
            (bold text), "italic" (italic text), "code" (monowidth string), "pre" (monowidth block), "text_link"
            (for clickable text URLs), "text_mention" (for custom text mentions based on users' identifiers).

        offset (``int``):
            Offset in UTF-16 code units to the start of the entity.

        length (``int``):
            Length of the entity in UTF-16 code units.

        url (``str``, *optional*):
            For "text_link" only, url that will be opened after user taps on the text.

        user (:obj:`User`, *optional*):
            For "text_mention" only, the mentioned user.
    """

    ENTITIES = {
        types.MessageEntityMention.ID: "mention",
        types.MessageEntityHashtag.ID: "hashtag",
        types.MessageEntityCashtag.ID: "cashtag",
        types.MessageEntityBotCommand.ID: "bot_command",
        types.MessageEntityUrl.ID: "url",
        types.MessageEntityEmail.ID: "email",
        types.MessageEntityBold.ID: "bold",
        types.MessageEntityItalic.ID: "italic",
        types.MessageEntityCode.ID: "code",
        types.MessageEntityPre.ID: "pre",
        types.MessageEntityUnderline.ID: "underline",
        types.MessageEntityStrike.ID: "strike",
        types.MessageEntityBlockquote.ID: "blockquote",
        types.MessageEntityTextUrl.ID: "text_link",
        types.MessageEntityMentionName.ID: "text_mention",
        types.MessageEntityPhone.ID: "phone_number"
    }

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        type: str,
        offset: int,
        length: int,
        url: str = None,
        user: User = None
    ):
        super().__init__(client)

        self.type = type
        self.offset = offset
        self.length = length
        self.url = url
        self.user = user

    @staticmethod
    def _parse(client, entity, users: dict) -> "MessageEntity" or None:
        type = MessageEntity.ENTITIES.get(entity.ID, None)

        if type is None:
            return None

        return MessageEntity(
            type=type,
            offset=entity.offset,
            length=entity.length,
            url=getattr(entity, "url", None),
            user=User._parse(client, users.get(getattr(entity, "user_id", None), None)),
            client=client
        )

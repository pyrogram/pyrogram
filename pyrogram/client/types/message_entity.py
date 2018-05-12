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

from pyrogram.api.core import Object


class MessageEntity(Object):
    """This object represents one special entity in a text message.
    For example, hashtags, usernames, URLs, etc.

    Args:
        type (``str``):
            Type of the entity.
            Can be mention (@username), hashtag, bot_command, url, email, bold (bold text), italic (italic text),
            code (monowidth string), pre (monowidth block), text_link (for clickable text URLs),
            text_mention (for users without usernames).

        offset (``int``):
            Offset in UTF-16 code units to the start of the entity.

        length (``int``):
            Length of the entity in UTF-16 code units.

        url (``str``, *optional*):
            For "text_link" only, url that will be opened after user taps on the text.

        user (:obj:`User <pyrogram.User>`, *optional*):
            For "text_mention" only, the mentioned user.
    """

    ID = 0xb0700004

    def __init__(self, type: str, offset: int, length: int, url: str = None, user=None):
        self.type = type  # string
        self.offset = offset  # int
        self.length = length  # int
        self.url = url  # flags.0?string
        self.user = user  # flags.1?User

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


class User(Object):
    """This object represents a Telegram user or bot.

    Args:
        id (``int``):
            Unique identifier for this user or bot.

        is_bot (``bool``):
            True, if this user is a bot.

        first_name (``str``):
            User's or bot's first name.

        last_name (``str``, *optional*):
            User's or bot's last name.

        username (``str``, *optional*):
            User's or bot's username.

        language_code (``str``, *optional*):
            IETF language tag of the user's language.

        phone_number (``str``, *optional*):
            User's or bot's phone number.

        photo (:obj:`ChatPhoto <pyrogram.ChatPhoto>`, *optional*):
            User's or bot's current profile photo.
    """

    ID = 0xb0700001

    def __init__(
            self,
            id: int,
            is_bot: bool,
            first_name: str,
            last_name: str = None,
            username: str = None,
            language_code: str = None,
            phone_number: str = None,
            photo=None
    ):
        self.id = id
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.username = username
        self.language_code = language_code
        self.phone_number = phone_number
        self.photo = photo

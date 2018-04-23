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

    Attributes:
        ID: ``0xb0700001``

    Args:
        id (``int`` ``32-bit``):
            Unique identifier for this user or bot.

        is_bot (``bool``):
            True, if this user is a bot.

        first_name (``str``):
            User's or bot's first name.

        last_name (``str``, optional):
            User's or bot's last name.

        username (``str``, optional):
            User's or bot's username.

        language_code (``str``, optional):
            IETF language tag of the user's language.

    """
    ID = 0xb0700001

    def __init__(self, id, is_bot, first_name, last_name=None, username=None, language_code=None):
        self.id = id  # int
        self.is_bot = is_bot  # Bool
        self.first_name = first_name  # string
        self.last_name = last_name  # flags.0?string
        self.username = username  # flags.1?string
        self.language_code = language_code  # flags.2?string

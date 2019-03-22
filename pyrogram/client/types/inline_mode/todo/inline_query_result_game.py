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

from pyrogram.client.types.pyrogram_type import PyrogramType


class InlineQueryResultGame(PyrogramType):
    """Represents a Game.

    Attributes:
        ID: ``0xb0700010``

    Args:
        type (``str``):
            Type of the result, must be game.

        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        game_short_name (``str``):
            Short name of the game.

        reply_markup (:obj:`InlineKeyboardMarkup <pyrogram.types.InlineKeyboardMarkup>`, optional):
            Inline keyboard attached to the message.

    """
    ID = 0xb0700010

    def __init__(self, type: str, id: str, game_short_name: str, reply_markup=None):
        self.type = type  # string
        self.id = id  # string
        self.game_short_name = game_short_name  # string
        self.reply_markup = reply_markup  # flags.0?InlineKeyboardMarkup

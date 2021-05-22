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

import pyrogram
from pyrogram import raw
from ..object import Object


class Dice(Object):
    """A dice with a random value from 1 to 6 for currently supported base emoji.

    Parameters:
        emoji (``string``):
            Emoji on which the dice throw animation is based.

        value (``int``):
            Value of the dice, 1-6 for currently supported base emoji.
    """

    def __init__(self, *, client: "pyrogram.Client" = None, emoji: str, value: int):
        super().__init__(client)

        self.emoji = emoji
        self.value = value

    @staticmethod
    def _parse(client, dice: "raw.types.MessageMediaDice") -> "Dice":
        return Dice(
            emoji=dice.emoticon,
            value=dice.value,
            client=client
        )

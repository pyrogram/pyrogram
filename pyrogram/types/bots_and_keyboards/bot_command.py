#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from pyrogram import raw

from ..object import Object


class BotCommand(Object):
    """A bot command with the standard slash "/" prefix.

    Parameters:
        command (``str``):
            Text of the command; 1-32 characters.
            Can contain only lowercase English letters, digits and underscores.

        description (``str``):
            Description of the command; 1-256 characters.
    """

    def __init__(self, command: str, description: str):
        super().__init__()

        self.command = command
        self.description = description

    def write(self) -> "raw.types.BotCommand":
        return raw.types.BotCommand(
            command=self.command,
            description=self.description,
        )

    @staticmethod
    def read(c: "raw.types.BotCommand") -> "BotCommand":
        return BotCommand(
            command=c.command,
            description=c.description
        )

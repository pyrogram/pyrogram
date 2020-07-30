#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

from typing import Dict

from pyrogram.api import functions
from ...ext import BaseClient


class SetMyCommands(BaseClient):
    def set_my_commands(
        self,
        commands: Dict[str, str]
    ) -> bool:
        """Update your bot commands list ("/" icon in official Telegram clients).

        Parameters:
            commands (``dict``):
                The new bot commands list, in "command": "description" format.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python
                app.set_my_commands({"start": "View Pyrogram docs"})
        """

        return bool(
            self.send(
                functions.bots.SetBotCommands(
                    commands=[
                        types.BotCommand(command=command, description=description)
                        for command, description in commands.items()
                    ]
                )
            )
        )

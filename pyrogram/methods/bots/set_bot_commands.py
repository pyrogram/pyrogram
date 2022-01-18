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

from typing import Optional, List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class SetBotCommands(Scaffold):
    async def set_bot_commands(self, commands: Optional[List[types.BotCommand]]):
        """Set the bot commands list.
        
        The commands passed will overwrite any command set previously.
        This method can be used by the own bot only.

        Parameters:
            commands (List of :obj:`~pyrogram.types.BotCommand`):
                A list of bot commands.
                Pass None to remove all commands.

        Returns:
            ``bool``: True on success, False otherwise.

        Example:
            .. code-block:: python
                
                from pyrogram.types import BotCommand
                
                # Set new commands
                app.set_bot_commands([
                    BotCommand("start", "Start the bot"),
                    BotCommand("settings", "Bot settings")])
                
                # Remove commands
                app.set_bot_commands(None)
        """

        return await self.send(
            raw.functions.bots.SetBotCommands(
                commands=[c.write() for c in commands or []]
            )
        )

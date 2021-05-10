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

from typing import Union, List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class SetBotCommands(Scaffold):
    async def set_bot_commands(
            self,
            commands: Union[
                List[types.BotCommand],
                None
            ]
    ):
        """Set Bot's commands list.

        Parameters:
            commands (List of List of (``str``, ``str``) | :obj:`~pyrogram.types.BotCommandsList` | ``NoneType``):
                A list of commands to b appeared when clicking on '/' in an official client.

        Returns:
            True on success.

        Example:
            .. code-block:: python
                app.set_bot_commands(
                    [
                        pyrogram.types.BotCommand("start", "start the bot"),
                        pyrogram.types.BotCommand("stop", "stop the bot")
                    ]
                )
                # in order to remove all commands we can pass [] or None.
        """

        if isinstance(commands, list):
            commands_list = []
            for command in commands:
                commands_list.append(command.write())
        elif commands is None:
            commands_list = []
        else:
            raise ValueError("commands must be a list of pyrogram.types.BotCommand")
        if await self.send(
            raw.functions.bots.SetBotCommands(
                commands=commands_list
            )
        ):
            return True

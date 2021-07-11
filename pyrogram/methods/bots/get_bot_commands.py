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

from typing import List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class GetBotCommands(Scaffold):
    async def get_bot_commands(
        self,
        scope: types.BotCommandScope = None,
        language_code: str = ''
    ) -> List[types.BotCommand]:
        """Get the bot commands list.
        
        This method can be used by the own bot only.

        Parameters:
            scope (:obj:`~pyrogram.types.BotCommandScope`):
                Scope of users. Defaults to :obj:`~pyrogram.types.BotCommandScopeDefault`.

            language_code (``str``, *optional*):
                A two-letter ISO 639-1 language code or an empty string.

        Returns:
            List of :obj:`~pyrogram.types.BotCommand`: On Success, the current list of bot's commands is returned
            for the given scope and user language. An empty list is returned if commands are not set.
        """
        if scope is None:
            scope = types.BotCommandScopeDefault()

        commands = await self.send(
            raw.functions.bots.GetBotCommands(
                scope=await scope.write(self),
                lang_code=language_code
            )
        )

        return types.List([types.BotCommand.read(c) for c in commands])

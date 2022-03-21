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
from pyrogram import types
from pyrogram.scaffold import Scaffold


class ResetBotCommands(Scaffold):
    async def reset_bot_commands(
        self,
        scope: types.BotCommandScope = None,
        language_code: str = ''
    ):
        """Reset the bot commands list.

        Parameters:
            scope (:obj:`~pyrogram.types.BotCommandScope`):
                Scope of users for which the commands are relevant. Defaults to :obj:`~pyrogram.types.BotCommandScopeDefault`.

            language_code (``str``, *optional*):
                A two-letter ISO 639-1 language code. If empty, commands will be applied to 
                all users from the given scope, for whose language there are no dedicated commands.

        Returns:
            ``bool``: True on success, False otherwise.
        """
        if scope is None:
            scope = types.BotCommandScopeDefault()

        return await self.send(
            raw.functions.bots.ResetBotCommands(
                scope=await scope.write(self),
                lang_code=language_code
            )
        )

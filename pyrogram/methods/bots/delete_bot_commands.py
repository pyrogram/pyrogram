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

import pyrogram
from pyrogram import raw, types
from pyrogram.scaffold import Scaffold


class DeleteBotCommands(Scaffold):
    async def delete_bot_commands(
        self: "pyrogram.Client",
        scope: "types.BotCommandScope" = types.BotCommandScopeDefault(),
        language_code: str = "",
    ):
        """Delete the list of the bot's commands for the given scope and user language.
        After deletion, higher level commands will be shown to affected users.

        The commands passed will overwrite any command set previously.
        This method can be used by the own bot only.

        Parameters:
            scope (:obj:`~pyrogram.types.BotCommandScope`, *optional*):
                An object describing the scope of users for which the commands are relevant.
                Defaults to :obj:`~pyrogram.types.BotCommandScopeDefault`.

            language_code (``str``, *optional*):
                A two-letter ISO 639-1 language code.
                If empty, commands will be applied to all users from the given scope, for whose language there are no
                dedicated commands.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Delete commands
                app.delete_bot_commands()
        """

        return await self.send(
            raw.functions.bots.ResetBotCommands(
                scope=await scope.write(self),
                lang_code=language_code,
            )
        )

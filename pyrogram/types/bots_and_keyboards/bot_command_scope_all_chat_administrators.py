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
from pyrogram import raw
from .bot_command_scope import BotCommandScope


class BotCommandScopeAllChatAdministrators(BotCommandScope):
    """Represents the scope of bot commands, covering all group and supergroup chat administrators.
    """

    def __init__(self):
        super().__init__("all_chat_administrators")

    async def write(self, client: "pyrogram.Client") -> "raw.base.BotCommandScope":
        return raw.types.BotCommandScopeChatAdmins()

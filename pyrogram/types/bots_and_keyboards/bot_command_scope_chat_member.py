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

from typing import Union

import pyrogram
from pyrogram import raw
from .bot_command_scope import BotCommandScope


class BotCommandScopeChatMember(BotCommandScope):
    """Represents the scope of bot commands, covering a specific member of a group or supergroup chat.

    Parameters:
        chat_id (``int`` | ``str``):
            Unique identifier for the target chat or username of the target supergroup (in the format
            @supergroupusername).

        user_id (``int`` | ``str``):
            Unique identifier of the target user.
    """

    def __init__(self, chat_id: Union[int, str], user_id: Union[int, str]):
        super().__init__("chat_member")

        self.chat_id = chat_id
        self.user_id = user_id

    async def write(self, client: "pyrogram.Client") -> "raw.base.BotCommandScope":
        return raw.types.BotCommandScopePeerUser(
            peer=await client.resolve_peer(self.chat_id),
            user_id=await client.resolve_peer(self.user_id)
        )

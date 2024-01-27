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
from pyrogram import types


class GetChatMenuButton:
    async def get_chat_menu_button(
        self: "pyrogram.Client",
        chat_id: Union[int, str] = None,
    ) -> "types.MenuButton":
        """Get the current value of the bot's menu button in a private chat, or the default menu button.

        .. include:: /_includes/usable-by/bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                If not specified, default bot's menu button will be returned.
        """

        if chat_id:
            r = await self.invoke(
                raw.functions.bots.GetBotMenuButton(
                    user_id=await self.resolve_peer(chat_id),
                )
            )
        else:
            r = (await self.invoke(
                raw.functions.users.GetFullUser(
                    id=raw.types.InputUserSelf()
                )
            )).full_user.bot_info.menu_button

        if isinstance(r, raw.types.BotMenuButtonCommands):
            return types.MenuButtonCommands()

        if isinstance(r, raw.types.BotMenuButtonDefault):
            return types.MenuButtonDefault()

        if isinstance(r, raw.types.BotMenuButton):
            return types.MenuButtonWebApp(
                text=r.text,
                web_app=types.WebAppInfo(
                    url=r.url
                )
            )

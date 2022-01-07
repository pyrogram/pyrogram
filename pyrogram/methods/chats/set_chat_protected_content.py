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

from pyrogram.raw import functions
from pyrogram.scaffold import Scaffold


class SetChatProtectedContent(Scaffold):
    async def set_chat_protected_content(
        self,
        chat_id: Union[int, str],
        enabled: bool
    ) -> bool:
        """Set the chat protected content setting.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            enabled (``bool``):
                Pass True to enable the protected content setting, False to disable.

        Returns:
            ``bool``: On success, True is returned.
        """

        await self.send(
            functions.messages.ToggleNoForwards(
                peer=await self.resolve_peer(chat_id),
                enabled=enabled
            )
        )

        return True

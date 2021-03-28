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

from typing import Optional, Union

from pyrogram import raw
from pyrogram.scaffold import Scaffold


class GetChatOnlines(Scaffold):
    async def get_chat_onlines(
        self,
        chat_id: Union[int, str]
    ) -> Optional[int]:
        """Get count of online users in a chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            ``int``: On success, the chat members online count is returned.

        Raises:
            ValueError: In case a chat id belongs to user.

        Example:
            .. code-block:: python

                onlines = app.get_chat_onlines("pyrogram")
                print(onlines)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, (raw.types.InputPeerChat, raw.types.InputPeerChannel)):
            r = await self.send(
                raw.functions.messages.GetOnlines(
                    peer=peer
                )
            )
            
            return r.onlines
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')
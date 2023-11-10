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

class UpdateColor:
    async def update_color(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        color: int,
        background_emoji_id: int = None
    ) -> "types.Chat":
        """Update color

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            color (``int``):
                Color

            background_emoji_id (``int``, *optional*):
                Background emoji

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                await app.update_color(chat_id, 1)
        """

        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerSelf):
            await self.invoke(
                raw.functions.account.UpdateColor(
                    color=color,
                    background_emoji_id=background_emoji_id
                )
            )

            r = await self.invoke(raw.functions.users.GetUsers(id=[raw.types.InputPeerSelf()]))
            return types.Chat._parse_user_chat(self, r[0])
        else:
            r = await self.invoke(
                raw.functions.channels.UpdateColor(
                    channel=peer,
                    color=color,
                    background_emoji_id=background_emoji_id
                )
            )

            return types.Chat._parse_channel_chat(self, r.chats[0])

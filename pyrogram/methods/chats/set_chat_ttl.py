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

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class SetChatTTL:
    async def set_chat_ttl(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        ttl_seconds: int
    ) -> "types.Message":
        """Set the time-to-live for the chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            ttl_seconds (``int``):
                The time-to-live for the chat.
                Either 86000 for 1 day, 604800 for 1 week or 0 (zero) to disable it.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Set TTL for a chat to 1 day
                app.set_chat_ttl(chat_id, 86400)

                # Set TTL for a chat to 1 week
                app.set_chat_ttl(chat_id, 604800)

                # Disable TTL for this chat
                app.set_chat_ttl(chat_id, 0)
        """
        r = await self.invoke(
            raw.functions.messages.SetHistoryTTL(
                peer=await self.resolve_peer(chat_id),
                period=ttl_seconds,
            )
        )

        for i in r.updates:
            if isinstance(i, (raw.types.UpdateNewMessage,
                              raw.types.UpdateNewChannelMessage)):
                return await types.Message._parse(
                    self,
                    i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats},
                )

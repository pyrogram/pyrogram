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

from typing import Union, Optional

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class SetChatHistoryTTL(Scaffold):
    async def set_chat_history_ttl(
        self, chat_id: Union[int, str], period: int
    ) -> "types.Message":
        """Set the time-to-live for the chat history.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            period (``int``):
                The time-to-live for the chat history.
                Either 86000 for 1 day, 604800 for 1 week or 0 (zero) to disable it.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the generated Service Message is returned.

        Example:
            .. code-block:: python

                # One Day
                app.set_chat_history_ttl(chat_id, 86400)

                # A Week
                app.set_chat_history_ttl(chat_id, 604800)

                # Disabling
                app.set_chat_history_ttl(chat_id, 0)
        """

        r = await self.send(
            raw.functions.messages.SetHistoryTTL(
                peer=await self.resolve_peer(chat_id),
                period=period,
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

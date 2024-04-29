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

from typing import Union, List, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetSimilarChannels:
    async def get_similar_channels(
        self: "pyrogram.Client",
        chat_id: Union[int, str]
    ) -> Optional[List["types.Chat"]]:
        """Get similar channels.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            List of :obj:`~pyrogram.types.Chat`: On success, the list of channels is returned.

        Example:
            .. code-block:: python

                channels = await app.get_similar_channels(chat_id)
                print(channels)
        """
        chat = await self.resolve_peer(chat_id)

        if isinstance(chat, raw.types.InputPeerChannel):
            r = await self.invoke(
                raw.functions.channels.GetChannelRecommendations(
                    channel=chat
                )
            )

            return types.List([types.Chat._parse_channel_chat(self, chat) for chat in r.chats]) or None
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user or chat')

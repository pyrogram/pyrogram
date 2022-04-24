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


class SetChatDescription:
    async def set_chat_description(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        description: str
    ) -> bool:
        """Change the description of a supergroup or a channel.
        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            description (``str``):
                New chat description, 0-255 characters.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: if a chat_id doesn't belong to a supergroup or a channel.

        Example:
            .. code-block:: python

                await app.set_chat_description(chat_id, "New Description")
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, (raw.types.InputPeerChannel, raw.types.InputPeerChat)):
            await self.invoke(
                raw.functions.messages.EditChatAbout(
                    peer=peer,
                    about=description
                )
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True

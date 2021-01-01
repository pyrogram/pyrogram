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

from pyrogram import raw
from pyrogram.scaffold import Scaffold


class DeleteChatPhoto(Scaffold):
    async def delete_chat_photo(
        self,
        chat_id: Union[int, str]
    ) -> bool:
        """Delete a chat photo.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: if a chat_id belongs to user.

        Example:
            .. code-block:: python

                app.delete_chat_photo(chat_id)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, raw.types.InputPeerChat):
            await self.send(
                raw.functions.messages.EditChatPhoto(
                    chat_id=peer.chat_id,
                    photo=raw.types.InputChatPhotoEmpty()
                )
            )
        elif isinstance(peer, raw.types.InputPeerChannel):
            await self.send(
                raw.functions.channels.EditPhoto(
                    channel=peer,
                    photo=raw.types.InputChatPhotoEmpty()
                )
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True

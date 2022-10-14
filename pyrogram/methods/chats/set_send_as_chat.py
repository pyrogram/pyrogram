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


class SetSendAsChat:
    async def set_send_as_chat(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        send_as_chat_id: Union[int, str]
    ) -> bool:
        """Set the default "send_as" chat for a chat.

        Use :meth:`~pyrogram.Client.get_send_as_chats` to get all the "send_as" chats available for use.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            send_as_chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the send_as chat.

        Returns:
            ``bool``: On success, true is returned

        Example:
            .. code-block:: python

                await app.set_send_as_chat(chat_id, send_as_chat_id)
        """
        return await self.invoke(
            raw.functions.messages.SaveDefaultSendAs(
                peer=await self.resolve_peer(chat_id),
                send_as=await self.resolve_peer(send_as_chat_id)
            )
        )

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


class DeleteUserHistory(Scaffold):
    async def delete_user_history(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
    ) -> bool:
        """Delete all messages sent by a certain user in a supergroup.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the user whose messages will be deleted.

        Returns:
            ``bool``: True on success, False otherwise.
        """

        r = await self.send(
            raw.functions.channels.DeleteUserHistory(
                channel=await self.resolve_peer(chat_id),
                user_id=await self.resolve_peer(user_id)
            )
        )

        # Deleting messages you don't have right onto won't raise any error.
        # Check for pts_count, which is 0 in case deletes fail.
        return bool(r.pts_count)

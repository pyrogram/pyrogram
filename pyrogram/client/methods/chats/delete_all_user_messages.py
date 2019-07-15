# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient


class DeleteAllUserMessages(BaseClient):
    def delete_all_user_messages(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
    ) -> bool:
        """Delete all of a user's messages in a chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                The user which you'd like all messages deleted.
                Pass the user_id as int or username as str.


        Returns:
            ``bool``: True on success, False otherwise.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        chat = self.resolve_peer(chat_id)
        user = self.resolve_peer(user_id)

        r = self.send(
            functions.channels.DeleteUserHistory(
                channel=chat,
                user_id=user
                )
            )

        # Deleting messages you don't have right onto, won't raise any error.
        # Check for pts_count, which is 0 in case deletes fail.
        return bool(r.pts_count)

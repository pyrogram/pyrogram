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
from ...ext import BaseClient


class UpdateChatUsername(BaseClient):
    def update_chat_username(
        self,
        chat_id: Union[int, str],
        username: Union[str, None]
    ) -> bool:
        """Use this method to update a channel or a supergroup username.
        
        To update your own username (for users only, not bots) you can use :meth:`update_username`.

        Args:
            chat_id (``int`` | ``str``)
                Unique identifier (int) or username (str) of the target chat.
            username (``str`` | ``None``):
                Username to set. Pass "" (empty string) or None to remove the username.

        Returns:
            True on success.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
            ``ValueError`` if a chat_id belongs to a user or chat.
        """

        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChannel):
            return bool(
                self.send(
                    functions.channels.UpdateUsername(
                        channel=peer,
                        username=username or ""
                    )
                )
            )
        else:
            raise ValueError("The chat_id \"{}\" belongs to a user or chat".format(chat_id))

# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

from pyrogram.api import functions, types
from ...ext import BaseClient


class SetChatDescription(BaseClient):
    def set_chat_description(self, chat_id: int or str, description: str):
        """Use this method to change the description of a supergroup or a channel.
        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            description (``str``):
                New chat description, 0-255 characters.

        Returns:
            True on success.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
            ``ValueError`` if a chat_id doesn't belong to a supergroup or a channel.
        """
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChannel):
            self.send(
                functions.channels.EditAbout(
                    channel=peer,
                    about=description
                )
            )
        elif isinstance(peer, types.InputPeerChat):
            raise ValueError("The chat_id \"{}\" belongs to a basic group".format(chat_id))
        else:
            raise ValueError("The chat_id \"{}\" belongs to a user".format(chat_id))

        return True

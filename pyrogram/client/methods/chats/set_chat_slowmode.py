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


class SetChatSlowmode(BaseClient):
    def set_chat_slowmode(
        self,
        chat_id: Union[int, str],
        seconds: int
    ) -> bool:
        """Set the slow mode in a supergroup. If it is enabled, users can only send one message in the specified time.
        Valid numbers of seconds are: 0 (disabled), 10, 30, 60, 300, 900, 3600
        
        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                
            seconds (``int``):
                Minimum number of seconds between two messages from the same user.
                
                
        Returns:
            ``bool``: True on success.
            
        Raises:
            ValueError: if the chat_id doesn't belong to a supergroup.
            BadRequest: if an invalid number of seconds is specified.
            ChatIdInvalid: if the chat_id belongs to a channel instead of a supergroup
            
        Example:
            .. code-block:: python

                app.set_chat_slowmode(chat_id, 30) # Set slow mode to 1 message per 30 seconds
                app.set_chat_slowmode(chat_id, 0) # Turn slow mode off
        """
        
        peer = self.resolve_peer(chat_id)
        
        if isinstance(peer, (types.InputPeerChannel, types.InputPeerChat)):
            self.send(
                functions.channels.ToggleSlowMode(
                    channel=peer,
                    seconds=seconds
                )
            )
        else:
            raise ValueError("The chat_id \"{}\" belongs to a user".format(chat_id))
            
        return True
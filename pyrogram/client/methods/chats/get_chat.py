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
from ...ext import BaseClient, utils


class GetChat(BaseClient):
    def get_chat(self, chat_id: int or str):
        """Use this method to get up to date information about the chat (current name of the user for
        one-on-one conversations, current username of a user, group or channel, etc.)

        Returns:
            On success, a :obj:`Chat <pyrogram.Chat>` object is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChannel):
            r = self.send(functions.channels.GetFullChannel(peer))
        elif isinstance(peer, (types.InputPeerUser, types.InputPeerSelf)):
            r = self.send(functions.users.GetFullUser(peer))
        else:
            r = self.send(functions.messages.GetFullChat(peer.chat_id))

        return utils.parse_chat_full(self, r)

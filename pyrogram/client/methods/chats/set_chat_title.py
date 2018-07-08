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


class SetChatTitle(BaseClient):
    def set_chat_title(self, chat_id: int or str, title: str):
        # TODO: Docstrings
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChat):
            self.send(
                functions.messages.EditChatTitle(
                    chat_id=peer.chat_id,
                    title=title
                )
            )
        elif isinstance(peer, types.InputPeerChannel):
            self.send(
                functions.channels.EditTitle(
                    channel=peer,
                    title=title
                )
            )
        else:
            raise ValueError("The chat_id \"{}\" belongs to a user".format(chat_id))

        return True

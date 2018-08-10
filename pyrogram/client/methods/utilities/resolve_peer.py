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

import re

from pyrogram.api import types, functions
from pyrogram.api.errors import PeerIdInvalid
from ...ext import BaseClient


class ResolvePeer(BaseClient):
    def resolve_peer(self, peer_id: int or str):
        """Use this method to get the InputPeer of a known peer_id.

        This is a utility method intended to be used only when working with Raw Functions (i.e: a Telegram API method
        you wish to use which is not available yet in the Client class as an easy-to-use method), whenever an InputPeer
        type is required.

        Args:
            peer_id (``int`` | ``str``):
                The peer id you want to extract the InputPeer from.
                Can be a direct id (int), a username (str) or a phone number (str).

        Returns:
            On success, the resolved peer id is returned in form of an InputPeer object.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        if type(peer_id) is str:
            if peer_id in ("self", "me"):
                return types.InputPeerSelf()

            peer_id = re.sub(r"[@+\s]", "", peer_id.lower())

            try:
                int(peer_id)
            except ValueError:
                if peer_id not in self.peers_by_username:
                    self.send(functions.contacts.ResolveUsername(peer_id))

                return self.peers_by_username[peer_id]
            else:
                try:
                    return self.peers_by_phone[peer_id]
                except KeyError:
                    raise PeerIdInvalid

        try:  # User
            return self.peers_by_id[peer_id]
        except KeyError:
            try:  # Chat
                return self.peers_by_id[-peer_id]
            except KeyError:
                try:  # Channel
                    return self.peers_by_id[int("-100" + str(peer_id))]
                except (KeyError, ValueError):
                    raise PeerIdInvalid

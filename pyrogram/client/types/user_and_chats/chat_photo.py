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

from struct import pack

import pyrogram
from pyrogram.api import types
from pyrogram.errors import PeerIdInvalid
from ..object import Object
from ...ext.utils import encode


class ChatPhoto(Object):
    """A chat photo.

    Parameters:
        small_file_id (``str``):
            File identifier of small (160x160) chat photo.
            This file_id can be used only for photo download and only for as long as the photo is not changed.

        big_file_id (``str``):
            File identifier of big (640x640) chat photo.
            This file_id can be used only for photo download and only for as long as the photo is not changed.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        small_file_id: str,
        big_file_id: str
    ):
        super().__init__(client)

        self.small_file_id = small_file_id
        self.big_file_id = big_file_id

    @staticmethod
    def _parse(client, chat_photo: types.UserProfilePhoto or types.ChatPhoto, peer_id: int):
        if not isinstance(chat_photo, (types.UserProfilePhoto, types.ChatPhoto)):
            return None

        photo_id = getattr(chat_photo, "photo_id", 0)
        loc_small = chat_photo.photo_small
        loc_big = chat_photo.photo_big

        try:
            peer = client.resolve_peer(peer_id)
        except PeerIdInvalid:
            return None

        if isinstance(peer, types.InputPeerUser):
            peer_id = peer.user_id
            peer_access_hash = peer.access_hash
            x = 0
        elif isinstance(peer, types.InputPeerChat):
            peer_id = -peer.chat_id
            peer_access_hash = 0
            x = -1
        else:
            peer_id += 1000727379968
            peer_access_hash = peer.access_hash
            x = -234

        return ChatPhoto(
            small_file_id=encode(
                pack(
                    "<iiqqqiiiqi",
                    1, chat_photo.dc_id, photo_id,
                    0, loc_small.volume_id,
                    2, peer_id, x, peer_access_hash, loc_small.local_id
                )
            ),
            big_file_id=encode(
                pack(
                    "<iiqqqiiiqi",
                    1, chat_photo.dc_id, photo_id,
                    0, loc_big.volume_id,
                    3, peer_id, x, peer_access_hash, loc_big.local_id
                )
            ),
            client=client
        )

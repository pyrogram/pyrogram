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
from ..object import Object
from ...ext.utils import encode


class ChatPhoto(Object):
    """A chat photo.

    Parameters:
        small_file_id (``str``):
            Unique file identifier of small (160x160) chat photo. This file_id can be used only for photo download.

        big_file_id (``str``):
            Unique file identifier of big (640x640) chat photo. This file_id can be used only for photo download.
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

        loc_small = chat_photo.photo_small
        loc_big = chat_photo.photo_big

        return ChatPhoto(
            small_file_id=encode(
                pack(
                    "<iiqqib",
                    1, chat_photo.dc_id, peer_id, loc_small.volume_id, loc_small.local_id, 0
                )
            ),
            big_file_id=encode(
                pack(
                    "<iiqqib",
                    1, chat_photo.dc_id, peer_id, loc_big.volume_id, loc_big.local_id, 1
                )
            ),
            client=client
        )

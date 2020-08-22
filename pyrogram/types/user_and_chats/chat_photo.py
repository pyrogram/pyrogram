#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

from struct import pack
from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram.utils import encode_file_id
from ..object import Object
from ... import utils


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
        client: "pyrogram.Client" = None,
        small_file_id: str,
        big_file_id: str
    ):
        super().__init__(client)

        self.small_file_id = small_file_id
        self.big_file_id = big_file_id

    @staticmethod
    def _parse(
        client,
        chat_photo: Union["raw.types.UserProfilePhoto", "raw.types.ChatPhoto"],
        peer_id: int,
        peer_access_hash: int
    ):
        if not isinstance(chat_photo, (raw.types.UserProfilePhoto, raw.types.ChatPhoto)):
            return None

        if peer_access_hash is None:
            return None

        photo_id = getattr(chat_photo, "photo_id", 0)
        loc_small = chat_photo.photo_small
        loc_big = chat_photo.photo_big

        peer_type = utils.get_peer_type(peer_id)

        if peer_type == "user":
            x = 0
        elif peer_type == "chat":
            x = -1
        else:
            peer_id += 1000727379968
            x = -234

        return ChatPhoto(
            small_file_id=encode_file_id(
                pack(
                    "<iiqqqiiiqi",
                    1, chat_photo.dc_id, photo_id,
                    0, loc_small.volume_id,
                    2, peer_id, x, peer_access_hash, loc_small.local_id
                )
            ),
            big_file_id=encode_file_id(
                pack(
                    "<iiqqqiiiqi",
                    1, chat_photo.dc_id, photo_id,
                    0, loc_big.volume_id,
                    3, peer_id, x, peer_access_hash, loc_big.local_id
                )
            ),
            client=client
        )

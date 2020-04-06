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
from typing import List

import pyrogram
from pyrogram.api import types
from .thumbnail import Thumbnail
from ..object import Object
from ...ext.utils import encode_file_id, encode_file_ref


class Photo(Object):
    """A Photo.

    Parameters:
        file_id (``str``):
            Unique identifier for this photo.

        file_ref (``str``):
            Up to date file reference.

        width (``int``):
            Photo width.

        height (``int``):
            Photo height.

        ttl_seconds (``int``):
            Time-to-live seconds, for secret photos.

        file_size (``int``):
            File size.

        date (``int``):
            Date the photo was sent in Unix time.

        thumbs (List of :obj:`Thumbnail`, *optional*):
            Available thumbnails of this photo.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        file_id: str,
        file_ref: str,
        width: int,
        height: int,
        ttl_seconds: int,
        file_size: int,
        date: int,
        thumbs: List[Thumbnail]
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.width = width
        self.height = height
        self.ttl_seconds = ttl_seconds
        self.file_size = file_size
        self.date = date
        self.thumbs = thumbs

    @staticmethod
    def _parse(client, photo: types.Photo, ttl_seconds: int = None) -> "Photo":
        if isinstance(photo, types.Photo):
            big = photo.sizes[-1]

            return Photo(
                file_id=encode_file_id(
                    pack(
                        "<iiqqqiiii",
                        2, photo.dc_id, photo.id, photo.access_hash,
                        big.location.volume_id, 1, 2, ord(big.type),
                        big.location.local_id
                    )
                ),
                file_ref=encode_file_ref(photo.file_reference),
                width=big.w,
                height=big.h,
                ttl_seconds=ttl_seconds,
                file_size=big.size,
                date=photo.date,
                thumbs=Thumbnail._parse(client, photo),
                client=client
            )

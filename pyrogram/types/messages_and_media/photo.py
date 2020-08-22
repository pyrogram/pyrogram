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
from pyrogram import raw
from pyrogram import types
from pyrogram.utils import encode_file_id, encode_file_ref
from ..object import Object


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

        file_size (``int``):
            File size.

        date (``int``):
            Date the photo was sent in Unix time.

        ttl_seconds (``int``, *optional*):
            Time-to-live seconds, for secret photos.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Available thumbnails of this photo.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_ref: str,
        width: int,
        height: int,
        file_size: int,
        date: int,
        ttl_seconds: int = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.width = width
        self.height = height
        self.file_size = file_size
        self.date = date
        self.ttl_seconds = ttl_seconds
        self.thumbs = thumbs

    @staticmethod
    def _parse(client, photo: "raw.types.Photo", ttl_seconds: int = None) -> "Photo":
        if isinstance(photo, raw.types.Photo):
            big = list(filter(lambda p: isinstance(p, raw.types.PhotoSize), photo.sizes))[-1]

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
                file_size=big.size,
                date=photo.date,
                ttl_seconds=ttl_seconds,
                thumbs=types.Thumbnail._parse(client, photo),
                client=client
            )

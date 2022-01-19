#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType, ThumbnailSource
from ..object import Object


class Photo(Object):
    """A Photo.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

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
        file_unique_id: str,
        width: int,
        height: int,
        file_size: int,
        date: int,
        ttl_seconds: int = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size
        self.date = date
        self.ttl_seconds = ttl_seconds
        self.thumbs = thumbs

    @staticmethod
    def _parse(client, photo: "raw.types.Photo", ttl_seconds: int = None) -> "Photo":
        if isinstance(photo, raw.types.Photo):
            photos: List[raw.types.PhotoSize] = []

            for p in photo.sizes:
                if isinstance(p, raw.types.PhotoSize):
                    photos.append(p)

                if isinstance(p, raw.types.PhotoSizeProgressive):
                    photos.append(
                        raw.types.PhotoSize(
                            type=p.type,
                            w=p.w,
                            h=p.h,
                            size=max(p.sizes)
                        )
                    )

            photos.sort(key=lambda p: p.size)

            main = photos[-1]

            return Photo(
                file_id=FileId(
                    file_type=FileType.PHOTO,
                    dc_id=photo.dc_id,
                    media_id=photo.id,
                    access_hash=photo.access_hash,
                    file_reference=photo.file_reference,
                    thumbnail_source=ThumbnailSource.THUMBNAIL,
                    thumbnail_file_type=FileType.PHOTO,
                    thumbnail_size=main.type,
                    volume_id=0,
                    local_id=0
                ).encode(),
                file_unique_id=FileUniqueId(
                    file_unique_type=FileUniqueType.DOCUMENT,
                    media_id=photo.id
                ).encode(),
                width=main.w,
                height=main.h,
                file_size=main.size,
                date=photo.date,
                ttl_seconds=ttl_seconds,
                thumbs=types.Thumbnail._parse(client, photo),
                client=client
            )

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

from typing import List, Optional, Union

import pyrogram
from pyrogram import raw
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType, ThumbnailSource
from ..object import Object


class Thumbnail(Object):
    """One size of a photo or a file/sticker thumbnail.

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
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        file_size: int
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @staticmethod
    def _parse(client, media: Union["raw.types.Photo", "raw.types.Document"]) -> Optional[List["Thumbnail"]]:
        if isinstance(media, raw.types.Photo):
            raw_thumbs = [i for i in media.sizes if isinstance(i, raw.types.PhotoSize)]
            raw_thumbs.sort(key=lambda p: p.size)
            raw_thumbs = raw_thumbs[:-1]

            file_type = FileType.PHOTO
        elif isinstance(media, raw.types.Document):
            raw_thumbs = media.thumbs
            file_type = FileType.THUMBNAIL
        else:
            return

        parsed_thumbs = []

        for thumb in raw_thumbs:
            if not isinstance(thumb, raw.types.PhotoSize):
                continue

            parsed_thumbs.append(
                Thumbnail(
                    file_id=FileId(
                        file_type=file_type,
                        dc_id=media.dc_id,
                        media_id=media.id,
                        access_hash=media.access_hash,
                        file_reference=media.file_reference,
                        thumbnail_file_type=file_type,
                        thumbnail_source=ThumbnailSource.THUMBNAIL,
                        thumbnail_size=thumb.type,
                        volume_id=0,
                        local_id=0
                    ).encode(),
                    file_unique_id=FileUniqueId(
                        file_unique_type=FileUniqueType.DOCUMENT,
                        media_id=media.id
                    ).encode(),
                    width=thumb.w,
                    height=thumb.h,
                    file_size=thumb.size,
                    client=client
                )
            )

        return parsed_thumbs or None

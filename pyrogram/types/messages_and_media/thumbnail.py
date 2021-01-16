#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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

from typing import Union, List, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types
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
    def _parse(
        client,
        media: Union["raw.types.Photo", "raw.types.Document"]
    ) -> Optional[List[Union["types.StrippedThumbnail", "Thumbnail"]]]:
        if isinstance(media, raw.types.Photo):
            raw_thumbnails = media.sizes[:-1]
        elif isinstance(media, raw.types.Document):
            raw_thumbnails = media.thumbs

            if not raw_thumbnails:
                return None
        else:
            return None

        thumbnails = []

        file_type = FileType.PHOTO if isinstance(media, raw.types.Photo) else FileType.THUMBNAIL
        thumbnail_file_type = file_type

        for thumbnail in raw_thumbnails:
            # TODO: Enable this
            # if isinstance(thumbnail, types.PhotoStrippedSize):
            #     thumbnails.append(StrippedThumbnail._parse(client, thumbnail))
            if isinstance(thumbnail, raw.types.PhotoSize):
                thumbnails.append(
                    Thumbnail(
                        file_id=FileId(
                            file_type=file_type,
                            dc_id=media.dc_id,
                            media_id=media.id,
                            access_hash=media.access_hash,
                            file_reference=media.file_reference,
                            thumbnail_file_type=thumbnail_file_type,
                            thumbnail_source=ThumbnailSource.THUMBNAIL,
                            thumbnail_size=thumbnail.type,
                            volume_id=thumbnail.location.volume_id,
                            local_id=thumbnail.location.local_id
                        ).encode(),
                        file_unique_id=FileUniqueId(
                            file_unique_type=FileUniqueType.PHOTO,
                            media_id=media.id,
                            volume_id=thumbnail.location.volume_id,
                            local_id=thumbnail.location.local_id
                        ).encode(),
                        width=thumbnail.w,
                        height=thumbnail.h,
                        file_size=thumbnail.size,
                        client=client
                    )
                )

        return thumbnails or None

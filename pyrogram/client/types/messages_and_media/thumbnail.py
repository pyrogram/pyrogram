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
from typing import Union, List

import pyrogram
from pyrogram.api import types
from pyrogram.client.ext.utils import encode
from .stripped_thumbnail import StrippedThumbnail
from ..pyrogram_type import PyrogramType


class Thumbnail(PyrogramType):
    """One size of a photo or a file/sticker thumbnail.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        width (``int``):
            Photo width.

        height (``int``):
            Photo height.

        file_size (``int``):
            File size.
    """

    __slots__ = ["file_id", "width", "height", "file_size"]

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        file_id: str,
        width: int,
        height: int,
        file_size: int
    ):
        super().__init__(client)

        self.file_id = file_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @staticmethod
    def _parse(
        client,
        media: Union[types.Photo, types.Document]
    ) -> Union[List[Union[StrippedThumbnail, "Thumbnail"]], None]:
        if isinstance(media, types.Photo):
            raw_thumbnails = media.sizes[:-1]
            media_type = 0
        elif isinstance(media, types.Document):
            raw_thumbnails = media.thumbs
            media_type = 14

            if not raw_thumbnails:
                return None
        else:
            return None

        thumbnails = []

        for thumbnail in raw_thumbnails:
            # TODO: Enable this
            # if isinstance(thumbnail, types.PhotoStrippedSize):
            #     thumbnails.append(StrippedThumbnail._parse(client, thumbnail))
            if isinstance(thumbnail, types.PhotoSize):
                thumbnails.append(
                    Thumbnail(
                        file_id=encode(
                            pack(
                                "<iiqqc",
                                media_type, media.dc_id,
                                media.id, media.access_hash,
                                thumbnail.type.encode()
                            )
                        ),
                        width=thumbnail.w,
                        height=thumbnail.h,
                        file_size=thumbnail.size,
                        client=client
                    )
                )

        return thumbnails or None

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
from typing import List

import pyrogram
from pyrogram.api import types
from .thumbnail import Thumbnail
from ..pyrogram_type import PyrogramType
from ...ext.utils import encode


class Photo(PyrogramType):
    """A Photo.

    Parameters:
        file_id (``str``):
            Unique identifier for this photo.

        width (``int``):
            Photo width.

        height (``int``):
            Photo height.

        file_size (``int``):
            File size.

        date (``int``):
            Date the photo was sent in Unix time.

        thumbnails (List of :obj:`Thumbnail`):
            Available sizes of this photo.
    """

    __slots__ = ["file_id", "width", "height", "file_size", "date", "thumbnails"]

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        file_id: str,
        width: int,
        height: int,
        file_size: int,
        date: int,
        thumbnails: List[Thumbnail]
    ):
        super().__init__(client)

        self.file_id = file_id
        self.width = width
        self.height = height
        self.file_size = file_size
        self.date = date
        self.thumbnails = thumbnails

    @staticmethod
    def _parse(client, photo: types.Photo) -> "Photo":
        if isinstance(photo, types.Photo):
            big = photo.sizes[-1]

            return Photo(
                file_id=encode(
                    pack(
                        "<iiqqc",
                        2, photo.dc_id,
                        photo.id, photo.access_hash,
                        big.type.encode()
                    )
                ),
                width=big.w,
                height=big.h,
                file_size=big.size,
                date=photo.date,
                thumbnails=Thumbnail._parse(client, photo),
                client=client
            )

# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

from base64 import b64encode
from struct import pack

from pyrogram.api import types
from .photo_size import PhotoSize
from ..pyrogram_type import PyrogramType
from ...ext.utils import encode


class Photo(PyrogramType):
    """This object represents a Photo.

    Args:
        id (``str``):
            Unique identifier for this photo.

        date (``int``):
            Date the photo was sent in Unix time.

        sizes (List of :obj:`PhotoSize <pyrogram.PhotoSize>`):
            Available sizes of this photo.
    """

    def __init__(self, *, client, raw, id: str, date: int, sizes: list):
        super().__init__(client, raw)

        self.id = id
        self.date = date
        self.sizes = sizes

    @staticmethod
    def parse(client, photo: types.Photo):
        if isinstance(photo, types.Photo):
            raw_sizes = photo.sizes
            sizes = []

            for raw_size in raw_sizes:
                if isinstance(raw_size, (types.PhotoSize, types.PhotoCachedSize)):

                    if isinstance(raw_size, types.PhotoSize):
                        file_size = raw_size.size
                    elif isinstance(raw_size, types.PhotoCachedSize):
                        file_size = len(raw_size.bytes)
                    else:
                        file_size = 0

                    loc = raw_size.location

                    if isinstance(loc, types.FileLocation):
                        size = PhotoSize(
                            file_id=encode(
                                pack(
                                    "<iiqqqqi",
                                    2, loc.dc_id, photo.id, photo.access_hash,
                                    loc.volume_id, loc.secret, loc.local_id)),
                            width=raw_size.w,
                            height=raw_size.h,
                            file_size=file_size,
                            client=client,
                            raw=raw_size
                        )

                        sizes.append(size)

            return Photo(
                id=b64encode(
                    pack(
                        "<qq",
                        photo.id,
                        photo.access_hash
                    ),
                    b"-_"
                ).decode().rstrip("="),
                date=photo.date,
                sizes=sizes,
                client=client,
                raw=photo
            )

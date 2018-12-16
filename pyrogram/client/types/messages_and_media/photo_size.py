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

from struct import pack

from pyrogram.api import types
from pyrogram.client.ext.utils import encode
from ..pyrogram_type import PyrogramType


class PhotoSize(PyrogramType):
    """This object represents one size of a photo or a file/sticker thumbnail.

    Args:
        file_id (``str``):
            Unique identifier for this file.

        width (``int``):
            Photo width.

        height (``int``):
            Photo height.

        file_size (``int``):
            File size.
    """

    def __init__(self, file_id: str, width: int, height: int, file_size: int, *,
                 client=None, raw=None):
        self.file_id = file_id
        self.width = width
        self.height = height
        self.file_size = file_size

        self._client = client
        self._raw = raw

    @staticmethod
    def parse(client, photo_size: types.PhotoSize or types.PhotoCachedSize):
        if isinstance(photo_size, (types.PhotoSize, types.PhotoCachedSize)):

            if isinstance(photo_size, types.PhotoSize):
                file_size = photo_size.size
            elif isinstance(photo_size, types.PhotoCachedSize):
                file_size = len(photo_size.bytes)
            else:
                file_size = 0

            loc = photo_size.location

            if isinstance(loc, types.FileLocation):
                return PhotoSize(
                    file_id=encode(
                        pack(
                            "<iiqqqqi",
                            0, loc.dc_id, 0, 0,
                            loc.volume_id, loc.secret, loc.local_id)),
                    width=photo_size.w,
                    height=photo_size.h,
                    file_size=file_size,
                    client=client,
                    raw=photo_size
                )

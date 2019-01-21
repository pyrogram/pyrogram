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
from typing import List, Union

import pyrogram
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

    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 file_id: str,
                 width: int,
                 height: int,
                 file_size: int):
        super().__init__(client)

        self.file_id = file_id
        self.width = width
        self.height = height
        self.file_size = file_size

    @staticmethod
    def _parse(client, thumbs: List) -> Union["PhotoSize", None]:
        if not thumbs:
            return None

        photo_size = thumbs[-1]

        if not isinstance(photo_size, (types.PhotoSize, types.PhotoCachedSize, types.PhotoStrippedSize)):
            return None

        loc = photo_size.location

        if not isinstance(loc, types.FileLocation):
            return None

        return PhotoSize(
            file_id=encode(
                pack(
                    "<iiqqqqi",
                    0, loc.dc_id, 0, 0,
                    loc.volume_id, loc.secret, loc.local_id
                )
            ),
            width=getattr(photo_size, "w", 0),
            height=getattr(photo_size, "h", 0),
            file_size=getattr(photo_size, "size", len(photo_size.bytes)),
            client=client
        )

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

from pyrogram.api.core import Object


class PhotoSize(Object):
    """This object represents one size of a photo or a file / sticker thumbnail.

    Args:
        file_id (``str``):
            Unique identifier for this file.

        width (``int``):
            Photo width.

        height (``int``):
            Photo height.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the photo was sent in Unix time
    """

    ID = 0xb0700005

    def __init__(self, file_id, width, height, file_size=None, date=None):
        self.file_id = file_id  # string
        self.width = width  # int
        self.height = height  # int
        self.file_size = file_size  # flags.0?int
        self.date = date

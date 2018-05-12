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


class ChatPhoto(Object):
    """This object represents a chat photo.

    Args:
        small_file_id (``str``):
            Unique file identifier of small (160x160) chat photo. This file_id can be used only for photo download.

        big_file_id (``str``):
            Unique file identifier of big (640x640) chat photo. This file_id can be used only for photo download.
    """

    ID = 0xb0700015

    def __init__(self, small_file_id: str, big_file_id: str):
        self.small_file_id = small_file_id  # string
        self.big_file_id = big_file_id  # string

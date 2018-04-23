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


class Voice(Object):
    """This object represents a voice note.

    Attributes:
        ID: ``0xb0700009``

    Args:
        file_id (``str``):
            Unique identifier for this file.

        duration (``int`` ``32-bit``):
            Duration of the audio in seconds as defined by sender.

        mime_type (``str``, optional):
            MIME type of the file as defined by sender.

        file_size (``int`` ``32-bit``, optional):
            File size.

    """
    ID = 0xb0700009

    def __init__(self, file_id, duration, mime_type=None, file_size=None):
        self.file_id = file_id  # string
        self.duration = duration  # int
        self.mime_type = mime_type  # flags.0?string
        self.file_size = file_size  # flags.1?int

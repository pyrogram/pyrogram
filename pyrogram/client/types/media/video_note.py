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


class VideoNote(Object):
    """This object represents a video message (available in Telegram apps as of v.4.0).

    Args:
        file_id (``str``):
            Unique identifier for this file.

        length (``int``):
            Video width and height as defined by sender.

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        thumb (:obj:`PhotoSize <pyrogram.PhotoSize>`, *optional*):
            Video thumbnail.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the video note was sent in Unix time.
    """

    ID = 0xb0700010

    def __init__(
            self,
            file_id: str,
            length: int,
            duration: int,
            thumb=None,
            mime_type: str = None,
            file_size: int = None,
            date: int = None
    ):
        self.file_id = file_id
        self.thumb = thumb
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.length = length
        self.duration = duration

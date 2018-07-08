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


class Audio(Object):
    """This object represents an audio file to be treated as music by the Telegram clients.

    Args:
        file_id (``str``):
            Unique identifier for this file.

        duration (``int``):
            Duration of the audio in seconds as defined by sender.

        thumb (:obj:`PhotoSize <pyrogram.PhotoSize>`, *optional*):
            Audio thumbnail.

        file_name (``str``, *optional*):
            Audio file name.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the audio was sent in Unix time.

        performer (``str``, *optional*):
            Performer of the audio as defined by sender or by audio tags.

        title (``str``, *optional*):
            Title of the audio as defined by sender or by audio tags.
    """

    ID = 0xb0700006

    def __init__(
            self,
            file_id: str,
            duration: int,
            thumb=None,
            file_name: str = None,
            mime_type: str = None,
            file_size: int = None,
            date: int = None,
            performer: str = None,
            title: str = None
    ):
        self.file_id = file_id  # string
        self.thumb = thumb  # flags.0?PhotoSize
        self.file_name = file_name  # flags.1?string
        self.mime_type = mime_type  # flags.2?string
        self.file_size = file_size  # flags.3?int
        self.date = date  # flags.4?int
        self.duration = duration  # int
        self.performer = performer  # flags.5?string
        self.title = title  # flags.6?string

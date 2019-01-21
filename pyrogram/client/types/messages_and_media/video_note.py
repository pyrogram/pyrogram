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

import pyrogram
from pyrogram.api import types
from .photo_size import PhotoSize
from ..pyrogram_type import PyrogramType
from ...ext.utils import encode


class VideoNote(PyrogramType):
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

    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 file_id: str,
                 length: int,
                 duration: int,
                 thumb: PhotoSize = None,
                 mime_type: str = None,
                 file_size: int = None,
                 date: int = None):
        super().__init__(client)

        self.file_id = file_id
        self.thumb = thumb
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.length = length
        self.duration = duration

    @staticmethod
    def _parse(client, video_note: types.Document, video_attributes: types.DocumentAttributeVideo) -> "VideoNote":
        return VideoNote(
            file_id=encode(
                pack(
                    "<iiqq",
                    13,
                    video_note.dc_id,
                    video_note.id,
                    video_note.access_hash
                )
            ),
            length=video_attributes.w,
            duration=video_attributes.duration,
            thumb=PhotoSize._parse(client, video_note.thumbs),
            file_size=video_note.size,
            mime_type=video_note.mime_type,
            date=video_note.date,
            client=client
        )

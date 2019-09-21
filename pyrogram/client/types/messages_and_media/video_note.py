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
from ..object import Object
from ...ext.utils import encode


class VideoNote(Object):
    """A video note.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        file_ref (``bytes``):
            Up to date file reference.

        length (``int``):
            Video width and height as defined by sender.

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the video note was sent in Unix time.

        thumbs (List of :obj:`Thumbnail`, *optional*):
            Video thumbnails.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        file_id: str,
        file_ref: bytes,
        length: int,
        duration: int,
        thumbs: List[Thumbnail] = None,
        mime_type: str = None,
        file_size: int = None,
        date: int = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.length = length
        self.duration = duration
        self.thumbs = thumbs

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
            file_ref=video_note.file_reference,
            length=video_attributes.w,
            duration=video_attributes.duration,
            file_size=video_note.size,
            mime_type=video_note.mime_type,
            date=video_note.date,
            thumbs=Thumbnail._parse(client, video_note),
            client=client
        )

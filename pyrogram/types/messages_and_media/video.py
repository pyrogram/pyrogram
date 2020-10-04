#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from struct import pack
from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.utils import encode_file_id, encode_file_ref
from ..object import Object


class Video(Object):
    """A video file.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        file_ref (``str``):
            Up to date file reference.

        width (``int``):
            Video width as defined by sender.

        height (``int``):
            Video height as defined by sender.

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        file_name (``str``, *optional*):
            Video file name.

        mime_type (``str``, *optional*):
            Mime type of a file as defined by sender.

        supports_streaming (``bool``, *optional*):
            True, if the video was uploaded with streaming support.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the video was sent in Unix time.

        ttl_seconds (``int``. *optional*):
            Time-to-live seconds, for secret photos.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Video thumbnails.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_ref: str,
        width: int,
        height: int,
        duration: int,
        file_name: str = None,
        mime_type: str = None,
        supports_streaming: bool = None,
        file_size: int = None,
        date: int = None,
        ttl_seconds: int = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.width = width
        self.height = height
        self.duration = duration
        self.file_name = file_name
        self.mime_type = mime_type
        self.supports_streaming = supports_streaming
        self.file_size = file_size
        self.date = date
        self.ttl_seconds = ttl_seconds
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        video: "raw.types.Document",
        video_attributes: "raw.types.DocumentAttributeVideo",
        file_name: str,
        ttl_seconds: int = None
    ) -> "Video":
        return Video(
            file_id=encode_file_id(
                pack(
                    "<iiqq",
                    4,
                    video.dc_id,
                    video.id,
                    video.access_hash
                )
            ),
            file_ref=encode_file_ref(video.file_reference),
            width=video_attributes.w,
            height=video_attributes.h,
            duration=video_attributes.duration,
            file_name=file_name,
            mime_type=video.mime_type,
            supports_streaming=video_attributes.supports_streaming,
            file_size=video.size,
            date=video.date,
            ttl_seconds=ttl_seconds,
            thumbs=types.Thumbnail._parse(client, video),
            client=client
        )

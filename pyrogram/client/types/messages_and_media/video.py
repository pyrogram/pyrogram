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


class Video(PyrogramType):
    """This object represents a video file.

    Args:
        file_id (``str``):
            Unique identifier for this file.

        width (``int``):
            Video width as defined by sender.

        height (``int``):
            Video height as defined by sender.

        duration (``int``):
            Duration of the video in seconds as defined by sender.

        thumb (:obj:`PhotoSize <pyrogram.PhotoSize>`, *optional*):
            Video thumbnail.

        file_name (``str``, *optional*):
            Video file name.

        mime_type (``str``, *optional*):
            Mime type of a file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the video was sent in Unix time.
    """

    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 file_id: str,
                 width: int,
                 height: int,
                 duration: int,
                 thumb: PhotoSize = None,
                 file_name: str = None,
                 mime_type: str = None,
                 file_size: int = None,
                 date: int = None):
        super().__init__(client)

        self.file_id = file_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.width = width
        self.height = height
        self.duration = duration

    @staticmethod
    def _parse(client, video: types.Document, video_attributes: types.DocumentAttributeVideo,
               file_name: str) -> "Video":
        return Video(
            file_id=encode(
                pack(
                    "<iiqq",
                    4,
                    video.dc_id,
                    video.id,
                    video.access_hash
                )
            ),
            width=video_attributes.w,
            height=video_attributes.h,
            duration=video_attributes.duration,
            thumb=PhotoSize._parse(client, video.thumb),
            mime_type=video.mime_type,
            file_size=video.size,
            file_name=file_name,
            date=video.date,
            client=client
        )

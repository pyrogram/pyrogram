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


class InputMediaVideo:
    """This object represents a video to be sent inside an album.
    It is intended to be used with :obj:`send_media_group() <pyrogram.Client.send_media_group>`.

    Args:
        media (``str``):
            Video to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine.
            Sending video by a URL is currently unsupported.

        caption (``str``, *optional*):
            Caption of the video to be sent, 0-200 characters

        parse_mode (``str``, *optional*):
            Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
            if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
            Defaults to Markdown.

        width (``int``, *optional*):
            Video width.

        height (``int``, *optional*):
            Video height.

        duration (``int``, *optional*):
            Video duration.

        supports_streaming (``bool``, *optional*):
            Pass True, if the uploaded video is suitable for streaming.
    """

    def __init__(self,
                 media: str,
                 caption: str = "",
                 parse_mode: str = "",
                 width: int = 0,
                 height: int = 0,
                 duration: int = 0,
                 supports_streaming: bool = True):
        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming

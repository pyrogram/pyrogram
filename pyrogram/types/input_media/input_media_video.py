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

from typing import Union

from .input_media import InputMedia


class InputMediaVideo(InputMedia):
    """A video to be sent inside an album.
    It is intended to be used with :obj:`~pyrogram.Client.send_media_group`.

    Parameters:
        media (``str``):
            Video to send.
            Pass a file_id as string to send a video that exists on the Telegram servers or
            pass a file path as string to upload a new video that exists on your local machine.
            Sending video by a URL is currently unsupported.

        file_ref (``str``, *optional*):
            A valid file reference obtained by a recently fetched media message.
            To be used in combination with a file id in case a file reference is needed.

        thumb (``str``):
            Thumbnail of the video sent.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

        caption (``str``, *optional*):
            Caption of the video to be sent, 0-1024 characters

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.

        width (``int``, *optional*):
            Video width.

        height (``int``, *optional*):
            Video height.

        duration (``int``, *optional*):
            Video duration.

        supports_streaming (``bool``, *optional*):
            Pass True, if the uploaded video is suitable for streaming.
    """

    def __init__(
        self,
        media: str,
        file_ref: str = None,
        thumb: str = None,
        caption: str = "",
        parse_mode: Union[str, None] = object,
        width: int = 0,
        height: int = 0,
        duration: int = 0,
        supports_streaming: bool = True
    ):
        super().__init__(media, file_ref, caption, parse_mode)

        self.thumb = thumb
        self.width = width
        self.height = height
        self.duration = duration
        self.supports_streaming = supports_streaming

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

from . import InputMedia


class InputMediaAudio(InputMedia):
    """This object represents an audio to be sent inside an album.
    It is intended to be used with :obj:`send_media_group() <pyrogram.Client.send_media_group>`.

    Args:
        media (``str``):
            Audio to send.
            Pass a file_id as string to send an audio that exists on the Telegram servers or
            pass a file path as string to upload a new audio that exists on your local machine.

        thumb (``str``, *optional*):
            Thumbnail of the music file album cover.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

        caption (``str``, *optional*):
            Caption of the audio to be sent, 0-1024 characters

        parse_mode (``str``, *optional*):
            Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
            if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
            Defaults to Markdown.

        duration (``int``, *optional*):
            Duration of the audio in seconds

        performer (``int``, *optional*):
            Performer of the audio

        title (``int``, *optional*):
            Title of the audio
    """

    __slots__ = ["thumb", "duration", "performer", "title"]

    def __init__(
        self,
        media: str,
        thumb: str = None,
        caption: str = "",
        parse_mode: str = "",
        duration: int = 0,
        performer: int = "",
        title: str = ""
    ):
        super().__init__(media, caption, parse_mode)

        self.thumb = thumb
        self.duration = duration
        self.performer = performer
        self.title = title

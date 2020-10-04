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


class InputMediaAudio(InputMedia):
    """An audio to be sent inside an album.

    It is intended to be used with :meth:`~pyrogram.Client.send_media_group`.

    Parameters:
        media (``str``):
            Audio to send.
            Pass a file_id as string to send an audio that exists on the Telegram servers or
            pass a file path as string to upload a new audio that exists on your local machine.

        file_ref (``str``, *optional*):
            A valid file reference obtained by a recently fetched media message.
            To be used in combination with a file id in case a file reference is needed.

        thumb (``str``, *optional*):
            Thumbnail of the music file album cover.
            The thumbnail should be in JPEG format and less than 200 KB in size.
            A thumbnail's width and height should not exceed 320 pixels.
            Thumbnails can't be reused and can be only uploaded as a new file.

        caption (``str``, *optional*):
            Caption of the audio to be sent, 0-1024 characters

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.

        duration (``int``, *optional*):
            Duration of the audio in seconds

        performer (``int``, *optional*):
            Performer of the audio

        title (``int``, *optional*):
            Title of the audio
    """

    def __init__(
        self,
        media: str,
        file_ref: str = None,
        thumb: str = None,
        caption: str = "",
        parse_mode: Union[str, None] = object,
        duration: int = 0,
        performer: str = "",
        title: str = ""
    ):
        super().__init__(media, file_ref, caption, parse_mode)

        self.thumb = thumb
        self.duration = duration
        self.performer = performer
        self.title = title

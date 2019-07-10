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

from typing import Union

from . import InputMedia


class InputMediaPhoto(InputMedia):
    """A photo to be sent inside an album.
    It is intended to be used with :obj:`send_media_group() <pyrogram.Client.send_media_group>`.

    Parameters:
        media (``str``):
            Photo to send.
            Pass a file_id as string to send a photo that exists on the Telegram servers or
            pass a file path as string to upload a new photo that exists on your local machine.
            Sending photo by a URL is currently unsupported.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters

        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.
    """

    __slots__ = []

    def __init__(
        self,
        media: str,
        caption: str = "",
        parse_mode: Union[str, None] = ""
    ):
        super().__init__(media, caption, parse_mode)

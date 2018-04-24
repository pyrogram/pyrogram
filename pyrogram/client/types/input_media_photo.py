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


class InputMediaPhoto:
    """This object represents a photo to be sent inside an album.
    It is intended to be used with :obj:`send_media_group() <pyrogram.Client.send_media_group>`.

    Args:
        media (``str``):
            Photo to send.
            Pass a file_id as string to send a photo that exists on the Telegram servers or
            pass a file path as string to upload a new photo that exists on your local machine.
            Sending photo by a URL is currently unsupported.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-200 characters

        parse_mode (``str``, *optional*):
            Use :obj:`MARKDOWN <pyrogram.ParseMode.MARKDOWN>` or :obj:`HTML <pyrogram.ParseMode.HTML>`
            if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in your caption.
            Defaults to Markdown.
    """

    def __init__(self,
                 media: str,
                 caption: str = "",
                 parse_mode: str = ""):
        self.media = media
        self.caption = caption
        self.parse_mode = parse_mode

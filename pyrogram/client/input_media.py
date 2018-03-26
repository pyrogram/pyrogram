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


class InputMedia:
    class Photo:
        """This object represents a photo to be sent inside an album.
        It is intended to be used with :obj:`pyrogram.Client.send_media_group`.

        Args:
            media (:obj:`str`):
                Photo file to send.
                Pass a file path as string to send a photo that exists on your local machine.

            caption (:obj:`str`):
                Caption of the photo to be sent, 0-200 characters

            parse_mode (:obj:`str`):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.
        """

        def __init__(self,
                     media: str,
                     caption: str = "",
                     parse_mode: str = ""):
            self.media = media
            self.caption = caption
            self.parse_mode = parse_mode

    class Video:
        """This object represents a video to be sent inside an album.
        It is intended to be used with :obj:`pyrogram.Client.send_media_group`.

        Args:
            media (:obj:`str`):
                Video file to send.
                Pass a file path as string to send a video that exists on your local machine.

            caption (:obj:`str`, optional):
                Caption of the video to be sent, 0-200 characters

            parse_mode (:obj:`str`, optional):
                Use :obj:`pyrogram.ParseMode.MARKDOWN` or :obj:`pyrogram.ParseMode.HTML` if you want Telegram apps
                to show bold, italic, fixed-width text or inline URLs in your caption.
                Defaults to Markdown.

            width (:obj:`int`, optional):
                Video width.

            height (:obj:`int`, optional):
                Video height

            duration (:obj:`int`, optional):
                Video duration.

            supports_streaming (:obj:`bool`, optional):
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

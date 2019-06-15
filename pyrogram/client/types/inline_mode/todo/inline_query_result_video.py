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

from pyrogram.client.types.object import Object


class InlineQueryResultVideo(Object):
    """Represents a link to a page containing an embedded video player or a video file. By default, this video file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the video.

    Attributes:
        ID: ``0xb0700003``

    Parameters:
        type (``str``):
            Type of the result, must be video.

        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        video_url (``str``):
            A valid URL for the embedded video player or video file.

        mime_type (``str``):
            Mime type of the content of video url, "text/html" or "video/mp4".

        thumb_url (``str``):
            URL of the thumbnail (jpeg only) for the video.

        title (``str``):
            Title for the result.

        caption (``str``, optional):
            Caption of the video to be sent, 0-200 characters.

        parse_mode (``str``, optional):
            Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.

        video_width (``int`` ``32-bit``, optional):
            Video width.

        video_height (``int`` ``32-bit``, optional):
            Video height.

        video_duration (``int`` ``32-bit``, optional):
            Video duration in seconds.

        description (``str``, optional):
            Short description of the result.

        reply_markup (:obj:`InlineKeyboardMarkup`, optional):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent`, optional):
            Content of the message to be sent instead of the video. This field is required if InlineQueryResultVideo is used to send an HTML-page as a result (e.g., a YouTube video).

    """
    ID = 0xb0700003

    def __init__(self, type: str, id: str, video_url: str, mime_type: str, thumb_url: str, title: str,
                 caption: str = None, parse_mode: str = None, video_width: int = None, video_height: int = None,
                 video_duration: int = None, description: str = None, reply_markup=None, input_message_content=None):
        self.type = type  # string
        self.id = id  # string
        self.video_url = video_url  # string
        self.mime_type = mime_type  # string
        self.thumb_url = thumb_url  # string
        self.title = title  # string
        self.caption = caption  # flags.0?string
        self.parse_mode = parse_mode  # flags.1?string
        self.video_width = video_width  # flags.2?int
        self.video_height = video_height  # flags.3?int
        self.video_duration = video_duration  # flags.4?int
        self.description = description  # flags.5?string
        self.reply_markup = reply_markup  # flags.6?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.7?InputMessageContent

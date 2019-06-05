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


class InlineQueryResultGif(Object):
    """Represents a link to an animated GIF file. By default, this animated GIF file will be sent by the user with optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the animation.

    Attributes:
        ID: ``0xb0700001``

    Parameters:
        type (``str``):
            Type of the result, must be gif.

        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        gif_url (``str``):
            A valid URL for the GIF file. File size must not exceed 1MB.

        thumb_url (``str``, optional):
            Width of the GIF.

        gif_width (``int`` ``32-bit``, optional):
            Height of the GIF.

        gif_height (``int`` ``32-bit``, optional):
            Duration of the GIF.

        gif_duration (``int`` ``32-bit``):
            URL of the static thumbnail for the result (jpeg or gif).

        title (``str``, optional):
            Title for the result.

        caption (``str``, optional):
            Caption of the GIF file to be sent, 0-200 characters.

        parse_mode (``str``, optional):
            Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.

        reply_markup (:obj:`InlineKeyboardMarkup <pyrogram.types.InlineKeyboardMarkup>`, optional):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent <pyrogram.types.InputMessageContent>`, optional):
            Content of the message to be sent instead of the GIF animation.

    """
    ID = 0xb0700001

    def __init__(self, type: str, id: str, gif_url: str, thumb_url: str, gif_width: int = None, gif_height: int = None, gif_duration: int = None, title: str = None, caption: str = None, parse_mode: str = None, reply_markup=None, input_message_content=None):
        self.type = type  # string
        self.id = id  # string
        self.gif_url = gif_url  # string
        self.gif_width = gif_width  # flags.0?int
        self.gif_height = gif_height  # flags.1?int
        self.gif_duration = gif_duration  # flags.2?int
        self.thumb_url = thumb_url  # string
        self.title = title  # flags.3?string
        self.caption = caption  # flags.4?string
        self.parse_mode = parse_mode  # flags.5?string
        self.reply_markup = reply_markup  # flags.6?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.7?InputMessageContent

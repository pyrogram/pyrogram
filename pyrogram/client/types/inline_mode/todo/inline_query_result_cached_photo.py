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


class InlineQueryResultCachedPhoto(Object):
    """Represents a link to a photo stored on the Telegram servers. By default, this photo will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.

    Attributes:
        ID: ``0xb0700011``

    Parameters:
        type (``str``):
            Type of the result, must be photo.

        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        photo_file_id (``str``):
            A valid file identifier of the photo.

        title (``str``, optional):
            Title for the result.

        description (``str``, optional):
            Short description of the result.

        caption (``str``, optional):
            Caption of the photo to be sent, 0-200 characters.

        parse_mode (``str``, optional):
            Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.

        reply_markup (:obj:`InlineKeyboardMarkup <pyrogram.types.InlineKeyboardMarkup>`, optional):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent <pyrogram.types.InputMessageContent>`, optional):
            Content of the message to be sent instead of the photo.

    """
    ID = 0xb0700011

    def __init__(self, type: str, id: str, photo_file_id: str, title: str = None, description: str = None, caption: str = None, parse_mode: str = None, reply_markup=None, input_message_content=None):
        self.type = type  # string
        self.id = id  # string
        self.photo_file_id = photo_file_id  # string
        self.title = title  # flags.0?string
        self.description = description  # flags.1?string
        self.caption = caption  # flags.2?string
        self.parse_mode = parse_mode  # flags.3?string
        self.reply_markup = reply_markup  # flags.4?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.5?InputMessageContent

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


class InlineQueryResultDocument(Object):
    """Represents a link to a file. By default, this file will be sent by the user with an optional caption. Alternatively, you can use input_message_content to send a message with the specified content instead of the file. Currently, only .PDF and .ZIP files can be sent using this method.

    Attributes:
        ID: ``0xb0700006``

    Parameters:
        type (``str``):
            Type of the result, must be document.

        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        title (``str``):
            Title for the result.

        document_url (``str``, optional):
            Caption of the document to be sent, 0-200 characters.

        mime_type (``str``, optional):
            Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.

        caption (``str``):
            A valid URL for the file.

        parse_mode (``str``):
            Mime type of the content of the file, either "application/pdf" or "application/zip".

        description (``str``, optional):
            Short description of the result.

        reply_markup (:obj:`InlineKeyboardMarkup`, optional):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent`, optional):
            Content of the message to be sent instead of the file.

        thumb_url (``str``, optional):
            URL of the thumbnail (jpeg only) for the file.

        thumb_width (``int`` ``32-bit``, optional):
            Thumbnail width.

        thumb_height (``int`` ``32-bit``, optional):
            Thumbnail height.

    """
    ID = 0xb0700006

    def __init__(self, type: str, id: str, title: str, document_url: str, mime_type: str, caption: str = None, parse_mode: str = None, description: str = None, reply_markup=None, input_message_content=None, thumb_url: str = None, thumb_width: int = None, thumb_height: int = None):
        self.type = type  # string
        self.id = id  # string
        self.title = title  # string
        self.caption = caption  # flags.0?string
        self.parse_mode = parse_mode  # flags.1?string
        self.document_url = document_url  # string
        self.mime_type = mime_type  # string
        self.description = description  # flags.2?string
        self.reply_markup = reply_markup  # flags.3?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.4?InputMessageContent
        self.thumb_url = thumb_url  # flags.5?string
        self.thumb_width = thumb_width  # flags.6?int
        self.thumb_height = thumb_height  # flags.7?int

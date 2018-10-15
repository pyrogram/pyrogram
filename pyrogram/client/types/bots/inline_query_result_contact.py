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

from pyrogram.api.core import Object


class InlineQueryResultContact(Object):
    """Represents a contact with a phone number. By default, this contact will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the contact.

    Attributes:
        ID: ``0xb0700009``

    Args:
        type (``str``):
            Type of the result, must be contact.

        id (``str``):
            Unique identifier for this result, 1-64 Bytes.

        phone_number (``str``):
            Contact's phone number.

        first_name (``str``):
            Contact's first name.

        last_name (``str``, optional):
            Contact's last name.

        vcard (``str``, optional):
            Additional data about the contact in the form of a vCard, 0-2048 bytes.

        reply_markup (:obj:`InlineKeyboardMarkup <pyrogram.types.InlineKeyboardMarkup>`, optional):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent <pyrogram.types.InputMessageContent>`, optional):
            Content of the message to be sent instead of the contact.

        thumb_url (``str``, optional):
            Url of the thumbnail for the result.

        thumb_width (``int`` ``32-bit``, optional):
            Thumbnail width.

        thumb_height (``int`` ``32-bit``, optional):
            Thumbnail height.

    """
    ID = 0xb0700009

    def __init__(self, type: str, id: str, phone_number: str, first_name: str, last_name: str = None, vcard: str = None, reply_markup=None, input_message_content=None, thumb_url: str = None, thumb_width: int = None, thumb_height: int = None):
        self.type = type  # string
        self.id = id  # string
        self.phone_number = phone_number  # string
        self.first_name = first_name  # string
        self.last_name = last_name  # flags.0?string
        self.vcard = vcard  # flags.1?string
        self.reply_markup = reply_markup  # flags.2?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.3?InputMessageContent
        self.thumb_url = thumb_url  # flags.4?string
        self.thumb_width = thumb_width  # flags.5?int
        self.thumb_height = thumb_height  # flags.6?int

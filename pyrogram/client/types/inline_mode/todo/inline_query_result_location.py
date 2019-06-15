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


class InlineQueryResultLocation(Object):
    """Represents a location on a map. By default, the location will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the location.

    Attributes:
        ID: ``0xb0700007``

    Parameters:
        type (``str``):
            Type of the result, must be location.

        id (``str``):
            Unique identifier for this result, 1-64 Bytes.

        latitude (``float`` ``64-bit``):
            Location latitude in degrees.

        longitude (``float`` ``64-bit``):
            Location longitude in degrees.

        title (``str``):
            Location title.

        live_period (``int`` ``32-bit``, optional):
            Period in seconds for which the location can be updated, should be between 60 and 86400.

        reply_markup (:obj:`InlineKeyboardMarkup <pyrogram.types.InlineKeyboardMarkup>`, optional):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent <pyrogram.types.InputMessageContent>`, optional):
            Content of the message to be sent instead of the location.

        thumb_url (``str``, optional):
            Url of the thumbnail for the result.

        thumb_width (``int`` ``32-bit``, optional):
            Thumbnail width.

        thumb_height (``int`` ``32-bit``, optional):
            Thumbnail height.

    """
    ID = 0xb0700007

    def __init__(self, type: str, id: str, latitude: float, longitude: float, title: str, live_period: int = None,
                 reply_markup=None, input_message_content=None, thumb_url: str = None, thumb_width: int = None,
                 thumb_height: int = None):
        self.type = type  # string
        self.id = id  # string
        self.latitude = latitude  # double
        self.longitude = longitude  # double
        self.title = title  # string
        self.live_period = live_period  # flags.0?int
        self.reply_markup = reply_markup  # flags.1?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.2?InputMessageContent
        self.thumb_url = thumb_url  # flags.3?string
        self.thumb_width = thumb_width  # flags.4?int
        self.thumb_height = thumb_height  # flags.5?int

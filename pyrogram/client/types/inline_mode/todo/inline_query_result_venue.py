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

from pyrogram.client.types.pyrogram_type import PyrogramType


class InlineQueryResultVenue(PyrogramType):
    """Represents a venue. By default, the venue will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the venue.

    Attributes:
        ID: ``0xb0700008``

    Args:
        type (``str``):
            Type of the result, must be venue.

        id (``str``):
            Unique identifier for this result, 1-64 Bytes.

        latitude (``float`` ``64-bit``):
            Latitude of the venue location in degrees.

        longitude (``float`` ``64-bit``):
            Longitude of the venue location in degrees.

        title (``str``):
            Title of the venue.

        address (``str``):
            Address of the venue.

        foursquare_id (``str``, optional):
            Foursquare identifier of the venue if known.

        foursquare_type (``str``, optional):
            Foursquare type of the venue, if known. (For example, "arts_entertainment/default", "arts_entertainment/aquarium" or "food/icecream".).

        reply_markup (:obj:`InlineKeyboardMarkup <pyrogram.types.InlineKeyboardMarkup>`, optional):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent <pyrogram.types.InputMessageContent>`, optional):
            Content of the message to be sent instead of the venue.

        thumb_url (``str``, optional):
            Url of the thumbnail for the result.

        thumb_width (``int`` ``32-bit``, optional):
            Thumbnail width.

        thumb_height (``int`` ``32-bit``, optional):
            Thumbnail height.

    """
    ID = 0xb0700008

    def __init__(self, type: str, id: str, latitude: float, longitude: float, title: str, address: str, foursquare_id: str = None, foursquare_type: str = None, reply_markup=None, input_message_content=None, thumb_url: str = None, thumb_width: int = None, thumb_height: int = None):
        self.type = type  # string
        self.id = id  # string
        self.latitude = latitude  # double
        self.longitude = longitude  # double
        self.title = title  # string
        self.address = address  # string
        self.foursquare_id = foursquare_id  # flags.0?string
        self.foursquare_type = foursquare_type  # flags.1?string
        self.reply_markup = reply_markup  # flags.2?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.3?InputMessageContent
        self.thumb_url = thumb_url  # flags.4?string
        self.thumb_width = thumb_width  # flags.5?int
        self.thumb_height = thumb_height  # flags.6?int

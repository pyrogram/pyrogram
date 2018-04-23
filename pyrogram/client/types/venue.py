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


class Venue(Object):
    """This object represents a venue.

    Attributes:
        ID: ``0xb0700013``

    Args:
        location (:obj:`Location <pyrogram.types.Location>`):
            Venue location.

        title (``str``):
            Name of the venue.

        address (``str``):
            Address of the venue.

        foursquare_id (``str``, optional):
            Foursquare identifier of the venue.

    """
    ID = 0xb0700013

    def __init__(self, location, title, address, foursquare_id=None):
        self.location = location  # Location
        self.title = title  # string
        self.address = address  # string
        self.foursquare_id = foursquare_id  # flags.0?string

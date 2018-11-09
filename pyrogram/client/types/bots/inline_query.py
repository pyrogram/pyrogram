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


class InlineQuery(Object):
    """This object represents an incoming inline query.
    When the user sends an empty query, your bot could return some default or trending results

    Args:
        id (``str``):
            Unique identifier for this query.

        from_user (:obj:`User <pyrogram.User>`):
            Sender.

        query (``str``):
            Text of the query (up to 512 characters).

        offset (``str``):
            Offset of the results to be returned, can be controlled by the bot.

        location (:obj:`Location <pyrogram.Location>`. *optional*):
            Sender location, only for bots that request user location.
    """
    ID = 0xb0700032

    def __init__(
            self,
            client,
            id: str,
            from_user,
            query: str,
            offset: str,
            location=None,
    ):
        self._client = client
        self.id = id
        self.from_user = from_user
        self.query = query
        self.offset = offset
        self.location = location

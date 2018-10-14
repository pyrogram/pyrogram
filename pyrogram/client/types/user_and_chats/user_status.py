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


class UserStatus(Object):
    """This object represents a User status (Last Seen privacy)

    .. note::

        You won't see exact last seen timestamps for people with whom you don't share your own. Instead, you get
        "recently", "within_week", "within_month" or "long_time_ago" fields set.

    Args:
        online (``bool``):
            True if the user is online in this moment, None otherwise.
            If True, the "date" field will be also set containing the online expiration date (i.e.: the date when a
            user will automatically go offline in case of no action by his client).

        offline (``bool``):
            True if the user is offline and has the Last Seen privacy setting visible for everybody, None otherwise.
            If True, the "date" field will be also set containing the last seen date (i.e.: the date when a user
            was online the last time).

        recently (``bool``):
            True for users with hidden Last Seen privacy that have been online between 1 second and 2-3 days ago,
            None otherwise.

        within_week (``bool``):
            True for users with hidden Last Seen privacy that have been online between 2-3 and seven days ago,
            None otherwise.

        within_month (``bool``):
            True for users with hidden Last Seen privacy that have been online between 6-7 days and a month ago,
            None otherwise.

        long_time_ago (``bool``):
            True for users with hidden Last Seen privacy that have been online more than a month ago (this is also
            always shown to blocked users), None otherwise.

        date (``int``):
            Exact date in unix time. Available only in case "online" or "offline" equals to True.
    """

    ID = 0xb0700031

    def __init__(
            self,
            online: bool = None,
            offline: bool = None,
            recently: bool = None,
            within_week: bool = None,
            within_month: bool = None,
            long_time_ago: bool = None,
            date: int = None,
    ):
        self.online = online
        self.offline = offline
        self.recently = recently
        self.within_week = within_week
        self.within_month = within_month
        self.long_time_ago = long_time_ago
        self.date = date

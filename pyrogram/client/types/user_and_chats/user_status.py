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
    """This object represents a User last seen status
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

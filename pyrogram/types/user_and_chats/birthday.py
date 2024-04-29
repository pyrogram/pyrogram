#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Optional

from pyrogram import raw
from ..object import Object


class Birthday(Object):
    """Birthday information of a user.

    Parameters:
        day (``int``):
            Birthday day.

        month (``int``):
            Birthday month.

        year (``int``, *optional*):
            Birthday year.
    """

    def __init__(
        self,
        *,
        day: int,
        month: int,
        year: int = None

    ):
        self.day = day
        self.month = month
        self.year = year

    @staticmethod
    def _parse(
        birthday: "raw.types.Birthday" = None
    ) -> Optional["Birthday"]:
        if not birthday:
            return

        return Birthday(
            day=birthday.day,
            month=birthday.month,
            year=getattr(birthday, "year", None)
        )

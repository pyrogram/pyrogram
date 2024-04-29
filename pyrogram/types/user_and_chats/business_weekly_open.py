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

from pyrogram import raw
from ..object import Object


class BusinessWeeklyOpen(Object):
    """Business weekly open hours.

    Parameters:
        start_minute (``int``):
            Start minute of the working day.

        end_minute (``int``):
            End minute of the working day.
    """

    def __init__(
        self,
        *,
        start_minute: int,
        end_minute: int,

    ):
        self.start_minute = start_minute
        self.end_minute = end_minute

    @staticmethod
    def _parse(weekly_open: "raw.types.BusinessWeeklyOpen" = None) -> "BusinessWeeklyOpen":
        return BusinessWeeklyOpen(
            start_minute=weekly_open.start_minute,
            end_minute=weekly_open.end_minute,
        )

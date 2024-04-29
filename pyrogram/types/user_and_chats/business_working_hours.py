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

from typing import Optional, List

from pyrogram import types, raw
from ..object import Object


class BusinessWorkingHours(Object):
    """Business working hours.

    Parameters:
        timezone (``str``):
            Timezone of the business.

        working_hours (List of :obj:`~pyrogram.types.BusinessWeeklyOpen`):
            Working hours of the business.

        is_open_now (``bool``, *optional*):
            True, if the business is open now.
    """

    def __init__(
        self,
        *,
        timezone: str,
        working_hours: List["types.BusinessWeeklyOpen"],
        is_open_now: bool = None

    ):
        self.timezone = timezone
        self.is_open_now = is_open_now
        self.working_hours = working_hours

    @staticmethod
    def _parse(work_hours: "raw.types.BusinessWorkHours" = None) -> Optional["BusinessWorkingHours"]:
        if not work_hours:
            return None

        return BusinessWorkingHours(
            timezone=work_hours.timezone_id,
            working_hours=types.List(
                types.BusinessWeeklyOpen._parse(i) for i in work_hours.weekly_open
            ),
            is_open_now=getattr(work_hours, "open_now", None),
        )

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

from datetime import datetime
from typing import Optional, Union, List

from pyrogram import types, enums, raw, utils
from ..object import Object


class BusinessMessage(Object):
    """A Business message.

    Parameters:
        shortcut_id (``int``):
            ID of the shortcut.

        is_greeting (``bool``, *optional*):
            True, if the message is a greeting message.

        is_away (``bool``, *optional*):
            True, if the message is an away message.

        no_activity_days (``int``, *optional*):
            Period of inactivity after which the greeting message should be sent again.

        offline_only (``bool``, *optional*):
            Dont send the away message if you've recently been online.

        recipients (List of :obj:`~pyrogram.types.User`, *optional*):
            Recipients of the message.

        schedule (:obj:`~pyrogram.enums.BusinessSchedule`, *optional*):
            Schedule of the away message to be sent.

        start_date (:py:obj:`~datetime.datetime`, *optional*):
            Start date of the away message.

        end_date (:py:obj:`~datetime.datetime`, *optional*):
            End date of the away message.
    """

    def __init__(
        self,
        *,
        shortcut_id: int,
        is_greeting: bool = None,
        is_away: bool = None,
        no_activity_days: int = None,
        offline_only: bool = None,
        recipients: List["types.User"] = None,
        schedule: "enums.BusinessSchedule" = None,
        start_date: datetime = None,
        end_date: datetime = None,

    ):
        self.shortcut_id = shortcut_id
        self.is_greeting = is_greeting
        self.is_away = is_away
        self.no_activity_days = no_activity_days
        self.offline_only = offline_only
        self.recipients = recipients
        self.schedule = schedule
        self.start_date = start_date
        self.end_date = end_date

    @staticmethod
    def _parse(
        client,
        message: Union["raw.types.BusinessGreetingMessage", "raw.types.BusinessAwayMessage"] = None,
        users: dict = None
    ) -> Optional["BusinessMessage"]:
        if not message:
            return None

        schedule = None

        if isinstance(message, raw.types.BusinessAwayMessage):
            if isinstance(message.schedule, raw.types.BusinessAwayMessageScheduleAlways):
                schedule = enums.BusinessSchedule.ALWAYS
            elif isinstance(message.schedule, raw.types.BusinessAwayMessageScheduleOutsideWorkHours):
                schedule = enums.BusinessSchedule.OUTSIDE_WORK_HOURS
            elif isinstance(message.schedule, raw.types.BusinessAwayMessageScheduleCustom):
                schedule = enums.BusinessSchedule.CUSTOM

        return BusinessMessage(
            shortcut_id=message.shortcut_id,
            is_greeting=isinstance(message, raw.types.BusinessGreetingMessage),
            is_away=isinstance(message, raw.types.BusinessAwayMessage),
            no_activity_days=getattr(message, "no_activity_days", None),
            offline_only=getattr(message, "offline_only", None),
            recipients=types.BusinessRecipients._parse(client, message.recipients, users),
            schedule=schedule,
            start_date=utils.timestamp_to_datetime(message.schedule.start_date) if schedule == enums.BusinessSchedule.CUSTOM else None,
            end_date=utils.timestamp_to_datetime(message.schedule.end_date) if schedule == enums.BusinessSchedule.CUSTOM else None
        )

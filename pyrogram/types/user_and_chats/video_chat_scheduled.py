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

from pyrogram import raw, utils
from ..object import Object


class VideoChatScheduled(Object):
    """A service message about a voice chat scheduled in the chat.

    Parameters:
        start_date (:py:obj:`~datetime.datetime`):
            Point in time when the voice chat is supposed to be started by a chat administrator.
    """

    def __init__(
        self, *,
        start_date: datetime
    ):
        super().__init__()

        self.start_date = start_date

    @staticmethod
    def _parse(action: "raw.types.MessageActionGroupCallScheduled") -> "VideoChatScheduled":
        return VideoChatScheduled(start_date=utils.timestamp_to_datetime(action.schedule_date))

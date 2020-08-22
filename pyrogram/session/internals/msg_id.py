#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

from time import monotonic


class MsgId:
    reference_clock = monotonic()
    last_time = 0
    msg_id_offset = 0

    def __new__(cls, server_time: float = 0) -> int:
        now = monotonic() - cls.reference_clock + server_time
        cls.msg_id_offset = cls.msg_id_offset + 4 if now == cls.last_time else 0
        msg_id = int(now * 2 ** 32) + cls.msg_id_offset
        cls.last_time = now

        return msg_id

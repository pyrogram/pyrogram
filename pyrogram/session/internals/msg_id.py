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

from threading import Lock
from time import time


class MsgId:
    def __init__(self, delta_time: float = 0.0):
        self.delta_time = delta_time
        self.last_time = 0
        self.offset = 0
        self.lock = Lock()

    def __call__(self) -> int:
        with self.lock:
            now = time()
            self.offset = self.offset + 4 if now == self.last_time else 0
            msg_id = int((now + self.delta_time) * 2 ** 32) + self.offset
            self.last_time = now

            return msg_id

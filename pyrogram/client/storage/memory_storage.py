# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

import base64
import logging
import sqlite3
import struct

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)


class MemoryStorage(SQLiteStorage):
    def __init__(self, name: str):
        super().__init__(name)

    def open(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.create()

        if self.name != ":memory:":
            dc_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
                self.SESSION_STRING_FORMAT,
                base64.urlsafe_b64decode(
                    self.name + "=" * (-len(self.name) % 4)
                )
            )

            self.dc_id(dc_id)
            self.test_mode(test_mode)
            self.auth_key(auth_key)
            self.user_id(user_id)
            self.is_bot(is_bot)
            self.date(0)

    def delete(self):
        pass

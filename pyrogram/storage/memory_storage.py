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

import base64
import logging
import sqlite3
import struct

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)


class MemoryStorage(SQLiteStorage):
    def __init__(self, name: str):
        super().__init__(name)

    async def open(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.create()

        if self.name != ":memory:":
            dc_id, test_mode, auth_key, user_id, is_bot = struct.unpack(
                (self.SESSION_STRING_FORMAT if len(self.name) == MemoryStorage.SESSION_STRING_SIZE else
                 self.SESSION_STRING_FORMAT_64),
                base64.urlsafe_b64decode(
                    self.name + "=" * (-len(self.name) % 4)
                )
            )

            await self.dc_id(dc_id)
            await self.test_mode(test_mode)
            await self.auth_key(auth_key)
            await self.user_id(user_id)
            await self.is_bot(is_bot)
            await self.date(0)

    async def delete(self):
        pass

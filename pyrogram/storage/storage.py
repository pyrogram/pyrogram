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
import struct
from typing import List, Tuple


class Storage:
    OLD_SESSION_STRING_FORMAT = ">B?256sI?"
    OLD_SESSION_STRING_FORMAT_64 = ">B?256sQ?"
    SESSION_STRING_SIZE = 351
    SESSION_STRING_SIZE_64 = 356

    SESSION_STRING_FORMAT = ">BI?256sQ?"

    def __init__(self, name: str):
        self.name = name

    async def open(self):
        raise NotImplementedError

    async def save(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def delete(self):
        raise NotImplementedError

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        raise NotImplementedError

    async def get_peer_by_id(self, peer_id: int):
        raise NotImplementedError

    async def get_peer_by_username(self, username: str):
        raise NotImplementedError

    async def get_peer_by_phone_number(self, phone_number: str):
        raise NotImplementedError

    async def dc_id(self, value: int = object):
        raise NotImplementedError

    async def api_id(self, value: int = object):
        raise NotImplementedError

    async def test_mode(self, value: bool = object):
        raise NotImplementedError

    async def auth_key(self, value: bytes = object):
        raise NotImplementedError

    async def date(self, value: int = object):
        raise NotImplementedError

    async def user_id(self, value: int = object):
        raise NotImplementedError

    async def is_bot(self, value: bool = object):
        raise NotImplementedError

    async def export_session_string(self):
        packed = struct.pack(
            self.SESSION_STRING_FORMAT,
            await self.dc_id(),
            await self.api_id(),
            await self.test_mode(),
            await self.auth_key(),
            await self.user_id(),
            await self.is_bot()
        )

        return base64.urlsafe_b64encode(packed).decode().rstrip("=")

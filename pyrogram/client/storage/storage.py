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
import struct
from typing import List, Tuple


class Storage:
    SESSION_STRING_FORMAT = ">B?256sI?"
    SESSION_STRING_SIZE = 351

    def __init__(self, name: str):
        self.name = name

    def open(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def delete(self):
        raise NotImplementedError

    def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        raise NotImplementedError

    def get_peer_by_id(self, peer_id: int):
        raise NotImplementedError

    def get_peer_by_username(self, username: str):
        raise NotImplementedError

    def get_peer_by_phone_number(self, phone_number: str):
        raise NotImplementedError

    def dc_id(self, value: int = object):
        raise NotImplementedError

    def test_mode(self, value: bool = object):
        raise NotImplementedError

    def auth_key(self, value: bytes = object):
        raise NotImplementedError

    def date(self, value: int = object):
        raise NotImplementedError

    def user_id(self, value: int = object):
        raise NotImplementedError

    def is_bot(self, value: bool = object):
        raise NotImplementedError

    def export_session_string(self):
        return base64.urlsafe_b64encode(
            struct.pack(
                self.SESSION_STRING_FORMAT,
                self.dc_id(),
                self.test_mode(),
                self.auth_key(),
                self.user_id(),
                self.is_bot()
            )
        ).decode().rstrip("=")

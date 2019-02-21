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

from typing import Dict


class SessionStorageMixin:
    @property
    def dc_id(self) -> int:
        return self.session_storage.dc_id

    @dc_id.setter
    def dc_id(self, val):
        self.session_storage.dc_id = val

    @property
    def test_mode(self) -> bool:
        return self.session_storage.test_mode

    @test_mode.setter
    def test_mode(self, val):
        self.session_storage.test_mode = val

    @property
    def auth_key(self) -> bytes:
        return self.session_storage.auth_key

    @auth_key.setter
    def auth_key(self, val):
        self.session_storage.auth_key = val

    @property
    def user_id(self):
        return self.session_storage.user_id

    @user_id.setter
    def user_id(self, val) -> int:
        self.session_storage.user_id = val

    @property
    def date(self) -> int:
        return self.session_storage.date

    @date.setter
    def date(self, val):
        self.session_storage.date = val

    @property
    def peers_by_id(self) -> Dict[str, int]:
        return self.session_storage.peers_by_id

    @property
    def peers_by_username(self) -> Dict[str, int]:
        return self.session_storage.peers_by_username

    @property
    def peers_by_phone(self) -> Dict[str, int]:
        return self.session_storage.peers_by_phone

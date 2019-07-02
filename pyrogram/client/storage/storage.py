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

from async_property import async_property


class Storage:
    def __init__(self, name: str):
        self.name = name

    async def open(self):
        raise NotImplementedError

    async def save(self):
        raise NotImplementedError

    async def close(self):
        raise NotImplementedError

    async def update_peers(self, peers):
        raise NotImplementedError

    async def get_peer_by_id(self, peer_id):
        raise NotImplementedError

    async def get_peer_by_username(self, username):
        raise NotImplementedError

    async def get_peer_by_phone_number(self, phone_number):
        raise NotImplementedError

    async def export_session_string(self):
        raise NotImplementedError

    @async_property
    async def peers_count(self):
        raise NotImplementedError

    @async_property
    async def dc_id(self):
        raise NotImplementedError

    async def set_dc_id(self, value):
        raise NotImplementedError

    @async_property
    async def test_mode(self):
        raise NotImplementedError

    async def set_test_mode(self, value):
        raise NotImplementedError

    @async_property
    async def auth_key(self):
        raise NotImplementedError

    async def set_auth_key(self, value):
        raise NotImplementedError

    @async_property
    async def date(self):
        raise NotImplementedError

    async def set_date(self, value):
        raise NotImplementedError

    @async_property
    async def user_id(self):
        raise NotImplementedError

    async def set_user_id(self, value):
        raise NotImplementedError

    @async_property
    async def is_bot(self):
        raise NotImplementedError

    async def set_is_bot(self, value):
        raise NotImplementedError

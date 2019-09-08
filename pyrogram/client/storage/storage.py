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


class Storage:
    def __init__(self, name: str):
        self.name = name

    def open(self):
        raise NotImplementedError

    def save(self):
        raise NotImplementedError

    def close(self):
        raise NotImplementedError

    def destroy(self):
        raise NotImplementedError

    def update_peers(self, peers):
        raise NotImplementedError

    def get_peer_by_id(self, peer_id):
        raise NotImplementedError

    def get_peer_by_username(self, username):
        raise NotImplementedError

    def get_peer_by_phone_number(self, phone_number):
        raise NotImplementedError

    def export_session_string(self):
        raise NotImplementedError

    @property
    def peers_count(self):
        raise NotImplementedError

    @property
    def dc_id(self):
        raise NotImplementedError

    @dc_id.setter
    def dc_id(self, value):
        raise NotImplementedError

    @property
    def test_mode(self):
        raise NotImplementedError

    @test_mode.setter
    def test_mode(self, value):
        raise NotImplementedError

    @property
    def auth_key(self):
        raise NotImplementedError

    @auth_key.setter
    def auth_key(self, value):
        raise NotImplementedError

    @property
    def date(self):
        raise NotImplementedError

    @date.setter
    def date(self, value):
        raise NotImplementedError

    @property
    def user_id(self):
        raise NotImplementedError

    @user_id.setter
    def user_id(self, value):
        raise NotImplementedError

    @property
    def is_bot(self):
        raise NotImplementedError

    @is_bot.setter
    def is_bot(self, value):
        raise NotImplementedError

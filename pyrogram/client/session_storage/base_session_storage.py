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

import abc
from typing import Type

import pyrogram


class SessionDoesNotExist(Exception):
    pass


class BaseSessionStorage(abc.ABC):
    def __init__(self, client: 'pyrogram.client.BaseClient', session_data):
        self.client = client
        self.session_data = session_data
        self.dc_id = 1
        self.test_mode = None
        self.auth_key = None
        self.user_id = None
        self.date = 0
        self.peers_by_id = {}
        self.peers_by_username = {}
        self.peers_by_phone = {}

    @abc.abstractmethod
    def load_session(self):
        ...

    @abc.abstractmethod
    def save_session(self, sync=False):
        ...

    @abc.abstractmethod
    def sync_cleanup(self):
        ...


class BaseSessionConfig(abc.ABC):
    @property
    @abc.abstractmethod
    def session_storage_cls(self) -> Type[BaseSessionStorage]:
        ...

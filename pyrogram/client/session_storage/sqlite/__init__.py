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

import logging
import os
import sqlite3

import pyrogram
from ....api import types
from ...ext import utils
from .. import MemorySessionStorage, SessionDoesNotExist


log = logging.getLogger(__name__)

EXTENSION = '.session.sqlite3'
MIGRATIONS = ['0001']


class SQLiteSessionStorage(MemorySessionStorage):
    def __init__(self, client: 'pyrogram.client.ext.BaseClient', session_name: str):
        super(SQLiteSessionStorage, self).__init__(client)
        self._session_name = session_name
        self._conn = None  # type: sqlite3.Connection

    def _get_file_name(self, name: str):
        if not name.endswith(EXTENSION):
            name += EXTENSION
        return os.path.join(self._client.workdir, name)

    def _apply_migrations(self, new_db=False):
        migrations = MIGRATIONS.copy()
        if not new_db:
            cursor = self._conn.cursor()
            cursor.execute('select name from migrations')
            for row in cursor.fetchone():
                migrations.remove(row)
        for name in migrations:
            with open(os.path.join(os.path.dirname(__file__), '{}.sql'.format(name))) as script:
                self._conn.executescript(script.read())

    def load(self):
        file_path = self._get_file_name(self._session_name)
        log.info('Loading SQLite session from {}'.format(file_path))

        if os.path.isfile(file_path):
            self._conn = sqlite3.connect(file_path)
            self._apply_migrations()
        else:
            self._conn = sqlite3.connect(file_path)
            self._apply_migrations(new_db=True)

        cursor = self._conn.cursor()
        cursor.execute('select dc_id, test_mode, auth_key, user_id, "date", is_bot from sessions')
        row = cursor.fetchone()
        if not row:
            raise SessionDoesNotExist()

        self._dc_id = row[0]
        self._test_mode = bool(row[1])
        self._auth_key = row[2]
        self._user_id = row[3]
        self._date = row[4]
        self._is_bot = bool(row[5])

    def cache_peer(self, entity):
        peer_id = username = phone = access_hash = None

        if isinstance(entity, types.User):
            peer_id = entity.id
            username = entity.username.lower() if entity.username else None
            phone = entity.phone or None
            access_hash = entity.access_hash
        elif isinstance(entity, (types.Chat, types.ChatForbidden)):
            peer_id = -entity.id
            # input_peer = types.InputPeerChat(chat_id=entity.id)
        elif isinstance(entity, (types.Channel, types.ChannelForbidden)):
            peer_id = int('-100' + str(entity.id))
            username = entity.username.lower() if hasattr(entity, 'username') and entity.username else None
            access_hash = entity.access_hash

        self._conn.execute('insert or replace into peers_cache values (?, ?, ?, ?)',
                           (peer_id, access_hash, username, phone))

    def get_peer_by_id(self, val):
        cursor = self._conn.cursor()
        cursor.execute('select id, hash from peers_cache where id = ?', (val,))
        row = cursor.fetchone()
        if not row:
            raise KeyError(val)
        return utils.get_input_peer(row[0], row[1])

    def get_peer_by_username(self, val):
        cursor = self._conn.cursor()
        cursor.execute('select id, hash from peers_cache where username = ?', (val,))
        row = cursor.fetchone()
        if not row:
            raise KeyError(val)
        return utils.get_input_peer(row[0], row[1])

    def get_peer_by_phone(self, val):
        cursor = self._conn.cursor()
        cursor.execute('select id, hash from peers_cache where phone = ?', (val,))
        row = cursor.fetchone()
        if not row:
            raise KeyError(val)
        return utils.get_input_peer(row[0], row[1])

    def save(self, sync=False):
        log.info('Committing SQLite session')
        self._conn.execute('delete from sessions')
        self._conn.execute('insert into sessions values (?, ?, ?, ?, ?, ?)',
                           (self._dc_id, self._test_mode, self._auth_key, self._user_id, self._date, self._is_bot))
        self._conn.commit()

    def sync_cleanup(self):
        pass

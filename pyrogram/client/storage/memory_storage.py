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
import inspect
import logging
import sqlite3
import struct
import time
from pathlib import Path
from threading import Lock
from typing import List, Tuple

from pyrogram.api import types
from pyrogram.client.storage.storage import Storage

log = logging.getLogger(__name__)


class MemoryStorage(Storage):
    SCHEMA_VERSION = 1
    USERNAME_TTL = 8 * 60 * 60
    SESSION_STRING_FMT = ">B?256sI?"
    SESSION_STRING_SIZE = 351

    def __init__(self, name: str):
        super().__init__(name)

        self.conn = None  # type: sqlite3.Connection
        self.lock = Lock()

    def create(self):
        with self.lock, self.conn:
            with open(str(Path(__file__).parent / "schema.sql"), "r") as schema:
                self.conn.executescript(schema.read())

            self.conn.execute(
                "INSERT INTO version VALUES (?)",
                (self.SCHEMA_VERSION,)
            )

            self.conn.execute(
                "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?)",
                (1, None, None, 0, None, None)
            )

    def _import_session_string(self, session_string: str):
        decoded = base64.urlsafe_b64decode(session_string + "=" * (-len(session_string) % 4))
        return struct.unpack(self.SESSION_STRING_FMT, decoded)

    def export_session_string(self):
        packed = struct.pack(
            self.SESSION_STRING_FMT,
            self.dc_id,
            self.test_mode,
            self.auth_key,
            self.user_id,
            self.is_bot
        )

        return base64.urlsafe_b64encode(packed).decode().rstrip("=")

    # noinspection PyAttributeOutsideInit
    def open(self):
        self.conn = sqlite3.connect(":memory:", check_same_thread=False)
        self.create()

        if self.name != ":memory:":
            imported_session_string = self._import_session_string(self.name)

            self.dc_id, self.test_mode, self.auth_key, self.user_id, self.is_bot = imported_session_string
            self.date = 0

    # noinspection PyAttributeOutsideInit
    def save(self):
        self.date = int(time.time())

        with self.lock:
            self.conn.commit()

    def close(self):
        with self.lock:
            self.conn.close()

    def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        with self.lock:
            self.conn.executemany(
                "REPLACE INTO peers (id, access_hash, type, username, phone_number)"
                "VALUES (?, ?, ?, ?, ?)",
                peers
            )

    def clear_peers(self):
        with self.lock, self.conn:
            self.conn.execute(
                "DELETE FROM peers"
            )

    @staticmethod
    def _get_input_peer(peer_id: int, access_hash: int, peer_type: str):
        if peer_type in ["user", "bot"]:
            return types.InputPeerUser(
                user_id=peer_id,
                access_hash=access_hash
            )

        if peer_type == "group":
            return types.InputPeerChat(
                chat_id=-peer_id
            )

        if peer_type in ["channel", "supergroup"]:
            return types.InputPeerChannel(
                channel_id=int(str(peer_id)[4:]),
                access_hash=access_hash
            )

        raise ValueError("Invalid peer type: {}".format(peer_type))

    def get_peer_by_id(self, peer_id: int):
        r = self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE id = ?",
            (peer_id,)
        ).fetchone()

        if r is None:
            raise KeyError("ID not found: {}".format(peer_id))

        return self._get_input_peer(*r)

    def get_peer_by_username(self, username: str):
        r = self.conn.execute(
            "SELECT id, access_hash, type, last_update_on FROM peers WHERE username = ?",
            (username,)
        ).fetchone()

        if r is None:
            raise KeyError("Username not found: {}".format(username))

        if abs(time.time() - r[3]) > self.USERNAME_TTL:
            raise KeyError("Username expired: {}".format(username))

        return self._get_input_peer(*r[:3])

    def get_peer_by_phone_number(self, phone_number: str):
        r = self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE phone_number = ?",
            (phone_number,)
        ).fetchone()

        if r is None:
            raise KeyError("Phone number not found: {}".format(phone_number))

        return self._get_input_peer(*r)

    @property
    def peers_count(self):
        return self.conn.execute(
            "SELECT COUNT(*) FROM peers"
        ).fetchone()[0]

    def _get(self):
        attr = inspect.stack()[1].function

        return self.conn.execute(
            "SELECT {} FROM sessions".format(attr)
        ).fetchone()[0]

    def _set(self, value):
        attr = inspect.stack()[1].function

        with self.lock, self.conn:
            self.conn.execute(
                "UPDATE sessions SET {} = ?".format(attr),
                (value,)
            )

    @property
    def dc_id(self):
        return self._get()

    @dc_id.setter
    def dc_id(self, value):
        self._set(value)

    @property
    def test_mode(self):
        return self._get()

    @test_mode.setter
    def test_mode(self, value):
        self._set(value)

    @property
    def auth_key(self):
        return self._get()

    @auth_key.setter
    def auth_key(self, value):
        self._set(value)

    @property
    def date(self):
        return self._get()

    @date.setter
    def date(self, value):
        self._set(value)

    @property
    def user_id(self):
        return self._get()

    @user_id.setter
    def user_id(self, value):
        self._set(value)

    @property
    def is_bot(self):
        return self._get()

    @is_bot.setter
    def is_bot(self, value):
        self._set(value)

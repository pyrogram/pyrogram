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
import aiosqlite as sqlite3
import struct
import time
from pathlib import Path
from typing import List, Tuple

from pyrogram.api import types
from pyrogram.client.storage.storage import Storage, async_property

log = logging.getLogger(__name__)


class MemoryStorage(Storage):
    SCHEMA_VERSION = 1
    USERNAME_TTL = 8 * 60 * 60
    SESSION_STRING_FMT = ">B?256sI?"
    SESSION_STRING_SIZE = 351

    def __init__(self, name: str):
        super().__init__(name)

        self.conn = None  # type: sqlite3.Connection

    async def create(self):
        async with self.conn:
            with open(str(Path(__file__).parent / "schema.sql"), "r") as schema:
                await self.conn.executescript(schema.read())

            await self.conn.execute(
                "INSERT INTO version VALUES (?)",
                (self.SCHEMA_VERSION,)
            )

            await self.conn.execute(
                "INSERT INTO sessions VALUES (?, ?, ?, ?, ?, ?)",
                (1, None, None, 0, None, None)
            )

    def _import_session_string(self, session_string: str):
        decoded = base64.urlsafe_b64decode(session_string + "=" * (-len(session_string) % 4))
        return struct.unpack(self.SESSION_STRING_FMT, decoded)

    async def export_session_string(self):
        packed = struct.pack(
            self.SESSION_STRING_FMT,
            await self.dc_id,
            await self.test_mode,
            await self.auth_key,
            await self.user_id,
            await self.is_bot
        )

        return base64.urlsafe_b64encode(packed).decode().rstrip("=")

    # noinspection PyAttributeOutsideInit
    async def open(self):
        self.conn = sqlite3.connect(":memory:")
        await self.create()

        if self.name != ":memory:":
            imported_session_string = self._import_session_string(self.name)

            dc_id, test_mode, auth_key, user_id, is_bot = imported_session_string
            await self.set_dc_id(dc_id)
            await self.set_test_mode(test_mode)
            await self.set_auth_key(auth_key)
            await self.set_user_id(user_id)
            await self.set_is_bot(is_bot)
            await self.set_date(0)

    # noinspection PyAttributeOutsideInit
    async def save(self):
        date = int(time.time())
        await self.set_date(date)
        await self.conn.commit()

    async def close(self):
        await self.conn.close()

    async def update_peers(self, peers: List[Tuple[int, int, str, str, str]]):
        await self.conn.executemany(
                "REPLACE INTO peers (id, access_hash, type, username, phone_number)"
                "VALUES (?, ?, ?, ?, ?)",
                peers
            )

    async def clear_peers(self):
        async with self.conn:
            await self.conn.execute(
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

    async def get_peer_by_id(self, peer_id: int):
        cursor = await self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE id = ?",
            (peer_id,)
        )
        r = await cursor.fetchone()

        if r is None:
            raise KeyError("ID not found: {}".format(peer_id))

        return self._get_input_peer(*r)

    async def get_peer_by_username(self, username: str):
        cursor = await self.conn.execute(
            "SELECT id, access_hash, type, last_update_on FROM peers WHERE username = ?",
            (username,)
        )
        r = await cursor.fetchone()

        if r is None:
            raise KeyError("Username not found: {}".format(username))

        if abs(time.time() - r[3]) > self.USERNAME_TTL:
            raise KeyError("Username expired: {}".format(username))

        return self._get_input_peer(*r[:3])

    async def get_peer_by_phone_number(self, phone_number: str):
        cursor = await self.conn.execute(
            "SELECT id, access_hash, type FROM peers WHERE phone_number = ?",
            (phone_number,)
        )
        r = await cursor.fetchone()

        if r is None:
            raise KeyError("Phone number not found: {}".format(phone_number))

        return self._get_input_peer(*r)

    @async_property
    async def peers_count(self):
        cursor = await self.conn.execute(
            "SELECT COUNT(*) FROM peers"
        )
        r = await cursor.fetchone()
        return r[0]

    async def _get(self, attr):

        cursor = await self.conn.execute(
            "SELECT {} FROM sessions".format(attr)
        )
        r = await cursor.fetchone()
        return r[0]

    async def _set(self, attr, value):
        async with self.conn:
            await self.conn.execute(
                "UPDATE sessions SET {} = ?".format(attr),
                (value,)
            )

    @async_property
    async def dc_id(self):
        return await self._get("dc_id")

    async def set_dc_id(self, value):
        await self._set("dc_id", value)

    @async_property
    async def test_mode(self):
        return await self._get("test_mode")

    async def set_test_mode(self, value):
        await self._set("test_mode", value)

    @async_property
    async def auth_key(self):
        return await self._get("auth_key")

    async def set_auth_key(self, value):
        await self._set("auth_key", value)

    @async_property
    async def date(self):
        return await self._get("date")

    async def set_date(self, value):
        await self._set("date", value)

    @async_property
    async def user_id(self):
        return await self._get("user_id")

    async def set_user_id(self, value):
        await self._set("user_id", value)

    @async_property
    async def is_bot(self):
        return await self._get("is_bot")

    async def set_is_bot(self, value):
        await self._set("is_bot", value)

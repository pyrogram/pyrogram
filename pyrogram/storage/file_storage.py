#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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
import json
import logging
import os
import sqlite3
from pathlib import Path

from .sqlite_storage import SQLiteStorage

log = logging.getLogger(__name__)


class FileStorage(SQLiteStorage):
    FILE_EXTENSION = ".session"

    def __init__(self, name: str, workdir: Path):
        super().__init__(name)

        self.database = workdir / (self.name + self.FILE_EXTENSION)

    async def migrate_from_json(self, session_json: dict):
        await self.open()

        await self.dc_id(session_json["dc_id"])
        await self.test_mode(session_json["test_mode"])
        await self.auth_key(base64.b64decode("".join(session_json["auth_key"])))
        await self.user_id(session_json["user_id"])
        await self.date(session_json.get("date", 0))
        await self.is_bot(session_json.get("is_bot", False))

        peers_by_id = session_json.get("peers_by_id", {})
        peers_by_phone = session_json.get("peers_by_phone", {})

        peers = {}

        for k, v in peers_by_id.items():
            if v is None:
                type_ = "group"
            elif k.startswith("-100"):
                type_ = "channel"
            else:
                type_ = "user"

            peers[int(k)] = [int(k), int(v) if v is not None else None, type_, None, None]

        for k, v in peers_by_phone.items():
            peers[v][4] = k

        # noinspection PyTypeChecker
        await self.update_peers(peers.values())

    def _update_from_one_impl(self):
        with self.conn:
            self.conn.execute("DELETE FROM peers")

    async def update(self):
        version = await self.version()

        if version == 1:
            await self.loop.run_in_executor(self.executor, self._update_from_one_impl)
            version += 1

        await self.version(version)

    async def open(self):
        path = self.database
        file_exists = path.is_file()

        if file_exists:
            try:
                with open(str(path), encoding="utf-8") as f:
                    session_json = json.load(f)
            except ValueError:
                pass
            else:
                log.warning("JSON session storage detected! Converting it into an SQLite session storage...")

                path.rename(path.name + ".OLD")

                log.warning(f'The old session file has been renamed to "{path.name}.OLD"')

                await self.migrate_from_json(session_json)

                log.warning("Done! The session has been successfully converted from JSON to SQLite storage")

                return

        if Path(path.name + ".OLD").is_file():
            log.warning(f'Old session file detected: "{path.name}.OLD". You can remove this file now')

        self.conn = self.executor.submit(sqlite3.connect, path).result()

        if not file_exists:
            await self.create()
        else:
            await self.update()

    async def delete(self):
        os.remove(self.database)

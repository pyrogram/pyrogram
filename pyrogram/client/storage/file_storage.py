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
import json
import logging
import os
import sqlite3
from pathlib import Path
from sqlite3 import DatabaseError
from threading import Lock
from typing import Union

from .memory_storage import MemoryStorage

log = logging.getLogger(__name__)


class FileStorage(MemoryStorage):
    FILE_EXTENSION = ".session"

    def __init__(self, name: str, workdir: Path):
        super().__init__(name)

        self.workdir = workdir
        self.database = workdir / (self.name + self.FILE_EXTENSION)
        self.conn = None  # type: sqlite3.Connection
        self.lock = Lock()

    # noinspection PyAttributeOutsideInit
    def migrate_from_json(self, path: Union[str, Path]):
        log.warning("JSON session storage detected! Pyrogram will now convert it into an SQLite session storage...")

        with open(path, encoding="utf-8") as f:
            json_session = json.load(f)

        os.remove(path)

        self.open()

        self.dc_id = json_session["dc_id"]
        self.test_mode = json_session["test_mode"]
        self.auth_key = base64.b64decode("".join(json_session["auth_key"]))
        self.user_id = json_session["user_id"]
        self.date = json_session.get("date", 0)
        self.is_bot = json_session.get("is_bot", False)

        peers_by_id = json_session.get("peers_by_id", {})
        peers_by_phone = json_session.get("peers_by_phone", {})

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
        self.update_peers(peers.values())

        log.warning("Done! The session has been successfully converted from JSON to SQLite storage")

    def open(self):
        database_exists = os.path.isfile(self.database)

        self.conn = sqlite3.connect(
            str(self.database),
            timeout=1,
            check_same_thread=False
        )

        try:
            if not database_exists:
                self.create()

            with self.conn:
                self.conn.execute("VACUUM")
        except DatabaseError:
            self.migrate_from_json(self.database)

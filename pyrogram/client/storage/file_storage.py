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
from threading import Lock

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
    def migrate_from_json(self, session_json: dict):
        self.open()

        self.dc_id = session_json["dc_id"]
        self.test_mode = session_json["test_mode"]
        self.auth_key = base64.b64decode("".join(session_json["auth_key"]))
        self.user_id = session_json["user_id"]
        self.date = session_json.get("date", 0)
        self.is_bot = session_json.get("is_bot", False)

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
        self.update_peers(peers.values())

    def open(self):
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

                log.warning('The old session file has been renamed to "{}.OLD"'.format(path.name))

                self.migrate_from_json(session_json)

                log.warning("Done! The session has been successfully converted from JSON to SQLite storage")

                return

        if Path(path.name + ".OLD").is_file():
            log.warning('Old session file detected: "{}.OLD". You can remove this file now'.format(path.name))

        self.conn = sqlite3.connect(
            str(path),
            timeout=1,
            check_same_thread=False
        )

        if not file_exists:
            self.create()

        with self.conn:
            try:  # Python 3.6.0 (exactly this version) is bugged and won't successfully execute the vacuum
                self.conn.execute("VACUUM")
            except sqlite3.OperationalError:
                pass

    def delete(self):
        os.remove(self.database)

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
import shutil

import pyrogram
from ..ext import utils
from . import MemorySessionStorage, SessionDoesNotExist


log = logging.getLogger(__name__)

EXTENSION = '.session'


class JsonSessionStorage(MemorySessionStorage):
    def __init__(self, client: 'pyrogram.client.ext.BaseClient', session_name: str):
        super(JsonSessionStorage, self).__init__(client)
        self._session_name = session_name

    def _get_file_name(self, name: str):
        if not name.endswith(EXTENSION):
            name += EXTENSION
        return os.path.join(self._client.workdir, name)

    def load(self):
        file_path = self._get_file_name(self._session_name)
        log.info('Loading JSON session from {}'.format(file_path))

        try:
            with open(file_path, encoding='utf-8') as f:
                s = json.load(f)
        except FileNotFoundError:
            raise SessionDoesNotExist()

        self._dc_id = s["dc_id"]
        self._test_mode = s["test_mode"]
        self._auth_key = base64.b64decode("".join(s["auth_key"]))  # join split key
        self._user_id = s["user_id"]
        self._date = s.get("date", 0)
        self._is_bot = s.get('is_bot', self._is_bot)

    def save(self, sync=False):
        pass

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

        for k, v in s.get("peers_by_id", {}).items():
            self._peers_cache['i' + k] = utils.get_input_peer(int(k), v)

        for k, v in s.get("peers_by_username", {}).items():
            try:
                self._peers_cache['u' + k] = self.get_peer_by_id(v)
            except KeyError:
                pass

        for k, v in s.get("peers_by_phone", {}).items():
            try:
                self._peers_cache['p' + k] = self.get_peer_by_id(v)
            except KeyError:
                pass

    def save(self, sync=False):
        file_path = self._get_file_name(self._session_name)

        if sync:
            file_path += '.tmp'

        log.info('Saving JSON session to {}, sync={}'.format(file_path, sync))

        auth_key = base64.b64encode(self._auth_key).decode()
        auth_key = [auth_key[i: i + 43] for i in range(0, len(auth_key), 43)]  # split key in lines of 43 chars

        os.makedirs(self._client.workdir, exist_ok=True)

        data = {
            'dc_id': self._dc_id,
            'test_mode': self._test_mode,
            'auth_key': auth_key,
            'user_id': self._user_id,
            'date': self._date,
            'is_bot': self._is_bot,
            'peers_by_id': {
                k[1:]: getattr(v, "access_hash", None)
                for k, v in self._peers_cache.copy().items()
                if k[0] == 'i'
            },
            'peers_by_username': {
                k[1:]: utils.get_peer_id(v)
                for k, v in self._peers_cache.copy().items()
                if k[0] == 'u'
            },
            'peers_by_phone': {
                k[1:]: utils.get_peer_id(v)
                for k, v in self._peers_cache.copy().items()
                if k[0] == 'p'
            }
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

            f.flush()
            os.fsync(f.fileno())

        # execution won't be here if an error has occurred earlier
        if sync:
            shutil.move(file_path, self._get_file_name(self._session_name))

    def sync_cleanup(self):
        try:
            os.remove(self._get_file_name(self._session_name) + '.tmp')
        except OSError:
            pass

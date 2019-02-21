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

from ..ext import utils
from . import BaseSessionStorage, SessionDoesNotExist


log = logging.getLogger(__name__)


class JsonSessionStorage(BaseSessionStorage):
    def _get_file_name(self, name: str):
        if not name.endswith('.session'):
            name += '.session'
        return os.path.join(self.client.workdir, name)

    def load_session(self):
        file_path = self._get_file_name(self.session_data)
        log.info('Loading JSON session from {}'.format(file_path))

        try:
            with open(file_path, encoding='utf-8') as f:
                s = json.load(f)
        except FileNotFoundError:
            raise SessionDoesNotExist()

        self.dc_id = s["dc_id"]
        self.test_mode = s["test_mode"]
        self.auth_key = base64.b64decode("".join(s["auth_key"]))  # join split key
        self.user_id = s["user_id"]
        self.date = s.get("date", 0)
        self.is_bot = s.get('is_bot', self.client.is_bot)

        for k, v in s.get("peers_by_id", {}).items():
            self.peers_by_id[int(k)] = utils.get_input_peer(int(k), v)

        for k, v in s.get("peers_by_username", {}).items():
            peer = self.peers_by_id.get(v, None)

            if peer:
                self.peers_by_username[k] = peer

        for k, v in s.get("peers_by_phone", {}).items():
            peer = self.peers_by_id.get(v, None)

            if peer:
                self.peers_by_phone[k] = peer

    def save_session(self, sync=False):
        file_path = self._get_file_name(self.session_data)

        if sync:
            file_path += '.tmp'

        log.info('Saving JSON session to {}, sync={}'.format(file_path, sync))

        auth_key = base64.b64encode(self.auth_key).decode()
        auth_key = [auth_key[i: i + 43] for i in range(0, len(auth_key), 43)]  # split key in lines of 43 chars

        os.makedirs(self.client.workdir, exist_ok=True)

        data = {
            'dc_id': self.dc_id,
            'test_mode': self.test_mode,
            'auth_key': auth_key,
            'user_id': self.user_id,
            'date': self.date,
            'is_bot': self.is_bot,
            'peers_by_id': {
                k: getattr(v, "access_hash", None)
                for k, v in self.peers_by_id.copy().items()
            },
            'peers_by_username': {
                k: utils.get_peer_id(v)
                for k, v in self.peers_by_username.copy().items()
            },
            'peers_by_phone': {
                k: utils.get_peer_id(v)
                for k, v in self.peers_by_phone.copy().items()
            }
        }

        with open(file_path, "w", encoding="utf-8") as f:
            json.dump(data, f, indent=4)

            f.flush()
            os.fsync(f.fileno())

        # execution won't be here if an error has occurred earlier
        if sync:
            shutil.move(file_path, self._get_file_name(self.session_data))

    def sync_cleanup(self):
        try:
            os.remove(self._get_file_name(self.session_data) + '.tmp')
        except OSError:
            pass

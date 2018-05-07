# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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
import time
from threading import Thread, Event, Lock

from . import utils

log = logging.getLogger(__name__)


class Syncer:
    INTERVAL = 20

    clients = {}
    thread = None
    event = Event()
    lock = Lock()

    @classmethod
    def add(cls, client):
        with cls.lock:
            cls.sync(client)

            cls.clients[id(client)] = client

            if len(cls.clients) == 1:
                cls.start()

    @classmethod
    def remove(cls, client):
        with cls.lock:
            cls.sync(client)

            del cls.clients[id(client)]

            if len(cls.clients) == 0:
                cls.stop()

    @classmethod
    def start(cls):
        cls.event.clear()
        cls.thread = Thread(target=cls.worker, name=cls.__name__)
        cls.thread.start()

    @classmethod
    def stop(cls):
        cls.event.set()

    @classmethod
    def worker(cls):
        while True:
            cls.event.wait(cls.INTERVAL)

            if cls.event.is_set():
                break

            with cls.lock:
                for client in cls.clients.values():
                    cls.sync(client)

    @classmethod
    def sync(cls, client):
        temporary = os.path.join(client.workdir, "{}.sync".format(client.session_name))
        persistent = os.path.join(client.workdir, "{}.session".format(client.session_name))

        try:
            auth_key = base64.b64encode(client.auth_key).decode()
            auth_key = [auth_key[i: i + 43] for i in range(0, len(auth_key), 43)]

            data = dict(
                dc_id=client.dc_id,
                test_mode=client.test_mode,
                auth_key=auth_key,
                user_id=client.user_id,
                date=int(time.time()),
                peers_by_id={
                    k: getattr(v, "access_hash", None)
                    for k, v in client.peers_by_id.copy().items()
                },
                peers_by_username={
                    k: utils.get_peer_id(v)
                    for k, v in client.peers_by_username.copy().items()
                },
                peers_by_phone={
                    k: utils.get_peer_id(v)
                    for k, v in client.peers_by_phone.copy().items()
                }
            )

            os.makedirs(client.workdir, exist_ok=True)

            with open(temporary, "w", encoding="utf-8") as f:
                json.dump(data, f, indent=4)

                f.flush()
                os.fsync(f.fileno())
        except Exception as e:
            log.critical(e, exc_info=True)
        else:
            shutil.move(temporary, persistent)
            log.info("Synced {}".format(client.session_name))
        finally:
            try:
                os.remove(temporary)
            except OSError:
                pass

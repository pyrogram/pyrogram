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
        client.date = int(time.time())
        try:
            client.session_storage.save_session(sync=True)
        except Exception as e:
            log.critical(e, exc_info=True)
        else:
            log.info("Synced {}".format(client.session_name))
        finally:
            client.session_storage.sync_cleanup()

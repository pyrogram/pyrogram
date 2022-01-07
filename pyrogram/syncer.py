#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

import asyncio
import logging
import time

log = logging.getLogger(__name__)


class Syncer:
    INTERVAL = 20

    clients = {}
    event = None
    lock = None

    @classmethod
    async def add(cls, client):
        if cls.event is None:
            cls.event = asyncio.Event()

        if cls.lock is None:
            cls.lock = asyncio.Lock()

        async with cls.lock:
            await cls.sync(client)

            cls.clients[id(client)] = client

            if len(cls.clients) == 1:
                cls.start()

    @classmethod
    async def remove(cls, client):
        async with cls.lock:
            await cls.sync(client)

            del cls.clients[id(client)]

            if len(cls.clients) == 0:
                cls.stop()

    @classmethod
    def start(cls):
        cls.event.clear()
        asyncio.get_event_loop().create_task(cls.worker())

    @classmethod
    def stop(cls):
        cls.event.set()

    @classmethod
    async def worker(cls):
        while True:
            try:
                await asyncio.wait_for(cls.event.wait(), cls.INTERVAL)
            except asyncio.TimeoutError:
                async with cls.lock:
                    for client in cls.clients.values():
                        await cls.sync(client)
            else:
                break

    @classmethod
    async def sync(cls, client):
        try:
            start = time.time()
            await client.storage.save()
        except Exception as e:
            log.critical(e, exc_info=True)
        else:
            log.debug(f'Synced "{client.storage.name}" in {(time.time() - start) * 1000:.6} ms')

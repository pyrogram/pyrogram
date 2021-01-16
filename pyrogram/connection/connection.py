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

import asyncio
import logging

from typing import Optional

from .transport import *
from ..session.internals import DataCenter

log = logging.getLogger(__name__)


class Connection:
    MAX_RETRIES = 3

    MODES = {
        0: TCPFull,
        1: TCPAbridged,
        2: TCPIntermediate,
        3: TCPAbridgedO,
        4: TCPIntermediateO
    }

    def __init__(self, dc_id: int, test_mode: bool, ipv6: bool, proxy: dict, mode: int = 3):
        self.dc_id = dc_id
        self.test_mode = test_mode
        self.ipv6 = ipv6
        self.proxy = proxy
        self.address = DataCenter(dc_id, test_mode, ipv6)
        self.mode = self.MODES.get(mode, TCPAbridged)

        self.protocol = None  # type: TCP

    async def connect(self):
        for i in range(Connection.MAX_RETRIES):
            self.protocol = self.mode(self.ipv6, self.proxy)

            try:
                log.info("Connecting...")
                await self.protocol.connect(self.address)
            except OSError as e:
                log.warning(f"Unable to connect due to network issues: {e}")
                self.protocol.close()
                await asyncio.sleep(1)
            else:
                log.info("Connected! {} DC{} - IPv{} - {}".format(
                    "Test" if self.test_mode else "Production",
                    self.dc_id,
                    "6" if self.ipv6 else "4",
                    self.mode.__name__
                ))
                break
        else:
            log.warning("Connection failed! Trying again...")
            raise TimeoutError

    def close(self):
        self.protocol.close()
        log.info("Disconnected")

    async def send(self, data: bytes):
        try:
            await self.protocol.send(data)
        except Exception:
            raise OSError

    async def recv(self) -> Optional[bytes]:
        return await self.protocol.recv()

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

import logging
import threading
import time

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

    def __init__(self, dc_id: int, test_mode: bool, ipv6: bool, proxy: dict, mode: int = 1):
        self.ipv6 = ipv6
        self.proxy = proxy
        self.address = DataCenter(dc_id, test_mode, ipv6)
        self.mode = self.MODES.get(mode, TCPAbridged)

        self.lock = threading.Lock()
        self.connection = None

    def connect(self):
        for i in range(Connection.MAX_RETRIES):
            self.connection = self.mode(self.ipv6, self.proxy)

            try:
                log.info("Connecting...")
                self.connection.connect(self.address)
            except OSError as e:
                log.warning(e)  # TODO: Remove
                self.connection.close()
                time.sleep(1)
            else:
                log.info("Connected! IPv{} - {}".format(
                    "6" if self.ipv6 else "4",
                    self.mode.__name__
                ))
                break
        else:
            raise TimeoutError

    def close(self):
        self.connection.close()
        log.info("Disconnected")

    def send(self, data: bytes):
        with self.lock:
            self.connection.sendall(data)

    def recv(self) -> bytes or None:
        return self.connection.recvall()

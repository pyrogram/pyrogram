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
import socket
from collections import namedtuple

import socks

log = logging.getLogger(__name__)

Proxy = namedtuple("Proxy", ["enabled", "hostname", "port", "username", "password"])


class TCP(socks.socksocket):
    def __init__(self, proxy: Proxy):
        super().__init__()
        self.settimeout(10)
        self.proxy_enabled = False

        if proxy and proxy.enabled:
            self.proxy_enabled = True

            self.set_proxy(
                proxy_type=socks.SOCKS5,
                addr=proxy.hostname,
                port=proxy.port,
                username=proxy.username,
                password=proxy.password
            )

            log.info("Using proxy {}:{}".format(
                proxy.hostname,
                proxy.port
            ))

    def close(self):
        try:
            self.shutdown(socket.SHUT_RDWR)
        except OSError:
            pass
        finally:
            super().close()

    def recvall(self, length: int) -> bytes or None:
        data = b""

        while len(data) < length:
            try:
                packet = super().recv(length - len(data))
            except OSError:
                return None
            else:
                if packet:
                    data += packet
                else:
                    return None

        return data

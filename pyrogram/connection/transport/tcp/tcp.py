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

import ipaddress
import logging
import socket

try:
    import socks
except ImportError as e:
    e.msg = (
        "PySocks is missing and Pyrogram can't run without. "
        "Please install it using \"pip3 install pysocks\"."
    )

    raise e

log = logging.getLogger(__name__)


class TCP(socks.socksocket):
    def __init__(self, ipv6: bool, proxy: dict):
        if proxy.get("enabled", False):
            hostname = proxy.get("hostname", None)
            port = proxy.get("port", None)

            try:
                ip_address = ipaddress.ip_address(hostname)
            except ValueError:
                super().__init__(socket.AF_INET)
            else:
                if isinstance(ip_address, ipaddress.IPv6Address):
                    super().__init__(socket.AF_INET6)
                else:
                    super().__init__(socket.AF_INET)

            self.set_proxy(
                proxy_type=socks.SOCKS5,
                addr=hostname,
                port=port,
                username=proxy.get("username", None),
                password=proxy.get("password", None)
            )

            log.info("Using proxy {}:{}".format(hostname, port))
        else:
            super().__init__(
                socket.AF_INET6 if ipv6
                else socket.AF_INET
            )

        self.settimeout(10)

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

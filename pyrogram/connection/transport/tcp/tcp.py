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
import socket
import time

try:
    import python_socks
except ImportError:
    python_socks = None

try:
    import socks
except ImportError as e:
    if python_socks is None:
        e.msg = (
            "PySocks is missing and Pyrogram can't run without. "
            "Please install it using \"pip3 install pysocks\"."
        )

        raise e

log = logging.getLogger(__name__)


class TCP:
    TIMEOUT = 10

    def __init__(self, ipv6: bool, proxy: dict):
        self.socket = None

        self.reader = None
        self.writer = None

        self.lock = asyncio.Lock()
        self.loop = asyncio.get_event_loop()
        self.proxy = proxy
        self.ipv6 = ipv6

    @staticmethod
    def _parse_proxy(scheme, hostname, port, rdns=True, username=None, password=None):
        if isinstance(scheme, str):
            scheme = scheme.lower()

        # Always prefer `python_socks` when available
        if python_socks:
            from python_socks import ProxyType

            # We do the check for numerical values here
            # to be backwards compatible with PySocks proxy format,
            # (since socks.SOCKS5 == 2, socks.SOCKS4 == 1, socks.HTTP == 3)
            if scheme == ProxyType.SOCKS5 or scheme == 2 or scheme == "socks5":
                protocol = ProxyType.SOCKS5
            elif scheme == ProxyType.SOCKS4 or scheme == 1 or scheme == "socks4":
                protocol = ProxyType.SOCKS4
            elif scheme == ProxyType.HTTP or scheme == 3 or scheme == "http":
                protocol = ProxyType.HTTP
            else:
                raise ValueError("Unknown proxy protocol type: {}".format(scheme))

            # This tuple must be compatible with `python_socks`' `Proxy.create()` signature
            return protocol, hostname, port, username, password, rdns

        else:
            from socks import (
                SOCKS5,
                SOCKS4,
                HTTP,
            )

            if scheme == 2 or scheme == "socks5":
                protocol = SOCKS5
            elif scheme == 1 or scheme == "socks4":
                protocol = SOCKS4
            elif scheme == 3 or scheme == "http":
                protocol = HTTP
            else:
                raise ValueError("Unknown proxy protocol type: {}".format(scheme))

            # This tuple must be compatible with `PySocks`' `socksocket.set_proxy()` signature
            return protocol, hostname, port, rdns, username, password

    async def _proxy_connect(self, dest_ip: str, dest_port: int, timeout: int = TIMEOUT) -> socket.socket:
        if isinstance(self.proxy, (tuple, list)):
            parsed = self._parse_proxy(*self.proxy)
        elif isinstance(self.proxy, dict):
            parsed = self._parse_proxy(**self.proxy)
        else:
            raise TypeError("Proxy of unknown format: {}".format(type(self.proxy)))

        # Always prefer `python_socks` when available
        if python_socks:
            # python_socks internal errors are not inherited from
            # builtin IOError (just from Exception). Instead of adding those
            # in exceptions clauses everywhere through the code, we
            # rather monkey-patch them in place.
            python_socks._errors.ProxyError = ConnectionError
            python_socks._errors.ProxyConnectionError = ConnectionError
            python_socks._errors.ProxyTimeoutError = ConnectionError

            from python_socks.async_.asyncio import Proxy

            proxy = Proxy.create(*parsed)

            sock = await proxy.connect(
                dest_host=dest_ip,
                dest_port=dest_port,
                timeout=timeout
            )

            log.info(f"Connected to {self.proxy.get('scheme')} proxy {parsed[1]}:{parsed[2]} with python_socks")
        else:
            import socks

            # Here `address` represents destination address (not proxy), because of
            # the `PySocks` implementation of the connection routine.
            # IPv family is checked on proxy address, not destination address.
            if self.ipv6:
                mode, address = socket.AF_INET6, (dest_ip, dest_port, 0, 0)
            else:
                mode, address = socket.AF_INET, (dest_ip, dest_port)

            # Setup socket, proxy, timeout and bind it (if necessary).
            sock = socks.socksocket(mode, socket.SOCK_STREAM)
            sock.set_proxy(*parsed)
            sock.settimeout(timeout)

            # Actual TCP connection and negotiation performed here.
            await asyncio.wait_for(
                asyncio.get_event_loop().sock_connect(sock=sock, address=address),
                timeout=timeout
            )

            log.info(f"Connected to {self.proxy.get('scheme')} proxy {parsed[1]}:{parsed[2]} with PySocks")

        return sock

    async def connect(self, address: tuple):
        (ip_addr, port) = address

        if self.proxy:
            self.socket = await self._proxy_connect(ip_addr, port, timeout=TCP.TIMEOUT)
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(sock=self.socket),
                timeout=TCP.TIMEOUT
            )
        else:
            self.reader, self.writer = await asyncio.wait_for(
                asyncio.open_connection(
                    host=ip_addr,
                    port=port,
                ),
                timeout=TCP.TIMEOUT
            )

        await self.writer.drain()

    async def close(self):
        try:
            self.writer.close()
            await asyncio.wait_for(self.writer.wait_closed(), timeout=10)
        except AttributeError as e:
            if bool(self.socket):
                try:
                    self.socket.shutdown(socket.SHUT_RDWR)
                except OSError:
                    pass
                finally:
                    # A tiny sleep placed here helps avoiding .recv(n) hanging until the timeout.
                    # This is a workaround that seems to fix the occasional delayed stop of a client.
                    time.sleep(0.001)
                    self.socket.close()

    async def send(self, data: bytes):
        async with self.lock:
            try:
                if self.writer is not None:
                    self.writer.write(data)
                    await self.writer.drain()
            except Exception as e:
                log.info("Send exception: %s %s", type(e).__name__, e)
                raise OSError(e)

    async def recv(self, length: int = 0):
        data = b""

        while len(data) < length:
            try:
                chunk = await asyncio.wait_for(
                    self.reader.read(length - len(data)),
                    TCP.TIMEOUT
                )
            except (OSError, asyncio.TimeoutError):
                return None
            else:
                if chunk:
                    data += chunk
                else:
                    return None

        return data

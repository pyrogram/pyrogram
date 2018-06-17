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

import asyncio
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


class TCP:
    TIMEOUT = 10

    def __init__(self, proxy: dict):
        self.proxy = proxy

        self.socket = socks.socksocket()
        self.reader = None  # type: asyncio.StreamReader
        self.writer = None  # type: asyncio.StreamWriter

        self.socket.settimeout(TCP.TIMEOUT)
        self.proxy_enabled = proxy.get("enabled", False)

        if proxy and self.proxy_enabled:
            self.socket.set_proxy(
                proxy_type=socks.SOCKS5,
                addr=proxy.get("hostname", None),
                port=proxy.get("port", None),
                username=proxy.get("username", None),
                password=proxy.get("password", None)
            )

            log.info("Using proxy {}:{}".format(
                proxy.get("hostname", None),
                proxy.get("port", None)
            ))

    async def connect(self, address: tuple):
        self.socket.connect(address)
        self.reader, self.writer = await asyncio.open_connection(sock=self.socket)

    def close(self):
        try:
            self.writer.close()
        except AttributeError:
            try:
                self.socket.shutdown(socket.SHUT_RDWR)
            except OSError:
                pass
            finally:
                self.socket.close()

    async def send(self, data: bytes):
        self.writer.write(data)
        await self.writer.drain()

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

# class TCP(socks.socksocket):
#     def __init__(self, proxy: dict):
#         super().__init__()
#         self.settimeout(10)
#         self.proxy_enabled = proxy.get("enabled", False)
#
#         if proxy and self.proxy_enabled:
#             self.set_proxy(
#                 proxy_type=socks.SOCKS5,
#                 addr=proxy.get("hostname", None),
#                 port=proxy.get("port", None),
#                 username=proxy.get("username", None),
#                 password=proxy.get("password", None)
#             )
#
#             log.info("Using proxy {}:{}".format(
#                 proxy.get("hostname", None),
#                 proxy.get("port", None)
#             ))
#
#     def close(self):
#         try:
#             self.shutdown(socket.SHUT_RDWR)
#         except OSError:
#             pass
#         finally:
#             super().close()
#
#     def recvall(self, length: int) -> bytes or None:
#         data = b""
#
#         while len(data) < length:
#             try:
#                 packet = super().recv(length - len(data))
#             except OSError:
#                 return None
#             else:
#                 if packet:
#                     data += packet
#                 else:
#                     return None
#
#         return data

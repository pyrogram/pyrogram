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
import websocket
import sys
import contextvars
import functools
from websocket._exceptions import WebSocketException
from websocket._http import ProxyError,ProxyTimeoutError,ProxyConnectionError

async def to_thread(func, /, *args, **kwargs):
    loop = asyncio.get_running_loop()
    ctx = contextvars.copy_context()
    func_call = functools.partial(ctx.run, func, *args, **kwargs)
    return await loop.run_in_executor(None, func_call)

if sys.version_info.major == 3 and sys.version_info.minor < 9:
    asyncio.to_thread = to_thread

def extract_err_message(exception):
    if exception.args:
        return exception.args[0]
    else:
        return '' 

log = logging.getLogger(__name__)

class WEBSOCKET:
    TIMEOUT = 10

    def __init__(self, ipv6: bool, proxy: dict):
        self.socket = None

        self.lock = asyncio.Lock()
        self.loop = asyncio.get_event_loop()

        websocket.setdefaulttimeout(WEBSOCKET.TIMEOUT)
        self.socket = websocket.WebSocket()
        if proxy:
            self.proxy_type=proxy.get("scheme")
            self.http_proxy_host=proxy.get("hostname")
            self.http_proxy_port=proxy.get("port", None)
            log.info(f"Using proxy {self.http_proxy_host}")
        else:
            self.proxy_type=""
            self.http_proxy_host=""
            self.http_proxy_port=""

        self.data_buffer=b''
        self.isconnected=False

    async def pingtask(self):
        try:
            log.info(f"starting websocket ping task")
            while self.isconnected:
                await asyncio.to_thread(self.socket.ping)
                await asyncio.sleep(30)
        except Exception as e:
            log.error(f'{type(e).__name__}: {e}')

    async def connect(self, address: tuple):
        try:
            scheme = "wss" if address[1]==443 else "ws"
            if self.proxy_type:
                await asyncio.to_thread(self.socket.connect,f"{scheme}://{address[0]}:{address[1]}/apiws", http_proxy_host=self.http_proxy_host, http_proxy_port=self.http_proxy_port, proxy_type=self.proxy_type, timeout=WEBSOCKET.TIMEOUT)
            else:
                await asyncio.to_thread(self.socket.connect,f"{scheme}://{address[0]}:{address[1]}/apiws",timeout=WEBSOCKET.TIMEOUT)
            self.isconnected=True
            asyncio.create_task(self.pingtask())
        except (WebSocketException,ProxyError,ProxyTimeoutError,ProxyConnectionError) as e:
            raise OSError(extract_err_message(e))
        except Exception as e:
            log.error(f'{type(e).__name__}: {e}')
            raise e

    def close(self):
        self.isconnected=False
        try:
            self.socket.close()
        except (WebSocketException,ProxyError,ProxyTimeoutError,ProxyConnectionError) as e:
            raise OSError(extract_err_message(e))
        except Exception as e:
            log.error(f'{type(e).__name__}: {e}')
            raise e

    async def send(self, data: bytes):
        async with self.lock:
            try:
                await asyncio.to_thread(self.socket.send_binary, data)
            except (WebSocketException,ProxyError,ProxyTimeoutError,ProxyConnectionError) as e:
                raise OSError(extract_err_message(e))
            except Exception as e:
                log.error(f'{type(e).__name__}: {e}')
                raise e

    async def recv(self, length: int = 0):
        data = self.data_buffer + b""

        while len(data) < length:
            try:
                chunk = await asyncio.to_thread(self.socket.recv)
            except (WebSocketException,ProxyError,ProxyTimeoutError,ProxyConnectionError) as e:
                log.error(f'{type(e).__name__}: {e}')
                return None
            except Exception as e:
                raise e
            else:
                if chunk:
                    data += chunk
                else:
                    return None

        self.data_buffer = data[length:]+b''
        return data[:length]


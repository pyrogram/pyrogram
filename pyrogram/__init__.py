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

__version__ = "1.2.8"
__license__ = "GNU Lesser General Public License v3 or later (LGPLv3+)"
__copyright__ = "Copyright (C) 2017-2021 Dan <https://github.com/delivrance>"

from concurrent.futures.thread import ThreadPoolExecutor


class StopTransmission(StopAsyncIteration):
    pass


class StopPropagation(StopAsyncIteration):
    pass


class ContinuePropagation(StopAsyncIteration):
    pass


import asyncio

from . import raw, types, filters, handlers, emoji
from .client import Client
from .sync import idle

# Save the main thread loop for future references
main_event_loop = asyncio.get_event_loop()

CRYPTO_EXECUTOR_SIZE_THRESHOLD = 512

crypto_executor = ThreadPoolExecutor(1, thread_name_prefix="CryptoWorker")

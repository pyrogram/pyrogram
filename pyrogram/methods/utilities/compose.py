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
from typing import (
    List, Callable, Any, Awaitable
)

import pyrogram
from .idle import idle


async def compose(
    clients: List["pyrogram.Client"],
    on_startup: Callable[[Any, Any], Awaitable[Any]] = None,
    on_shutdown: Callable[[Any, Any], Awaitable[Any]] = None,
    sequential: bool = False
):
    """Run multiple clients at once.

    This method can be used to run multiple clients at once and can be found directly in the ``pyrogram`` package.

    If you want to run a single client, you can use Client's bound method :meth:`~pyrogram.Client.run`.

    Parameters:
        clients (List of :obj:`~pyrogram.Client`):
            A list of client objects to run.

        on_startup (``callable``, *optional*):
            Function to execute when clients run.

        on_shutdown (``callable``, *optional*):
            Function to execute when clients shutdown.

        sequential (``bool``, *optional*):
            Pass True to run clients sequentially.
            Defaults to False (run clients concurrently)

    Example:
        .. code-block:: python

            import asyncio
            from pyrogram import Client, compose


            async def main():
                apps = [
                    Client("account1"),
                    Client("account2"),
                    Client("account3")
                ]

                ...

                await compose(apps)


            asyncio.run(main())

    """
    if sequential:
        if on_startup:
            for c in clients:
                await c.start()
            await on_startup()
        else:
            for c in clients:
                await c.start()
    else:
        tasks = []
        if on_startup:
            for c in clients:
                tasks.append(c.start())
            tasks.append(on_startup())
        else:
            for c in clients:
                tasks.append(c.start())
        await asyncio.gather(*tasks)

    await idle()

    if sequential:
        if on_shutdown:
            for c in clients:
                await c.stop()
            await on_shutdown()
        else:
            for c in clients:
                await c.stop()
    else:
        tasks = []
        if on_shutdown:
            for c in clients:
                tasks.append(c.stop())
            tasks.append(on_shutdown())
        else:
            for c in clients:
                tasks.append(c.stop())
        await asyncio.gather(*tasks)

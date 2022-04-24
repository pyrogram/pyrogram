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

from typing import List

import pyrogram
from .idle import idle


async def compose(clients: List["pyrogram.Client"]):
    """Run multiple clients at once.

    This method can be used to run multiple clients at once and can be found directly in the ``pyrogram`` package.

    If you want to run a single client, you can use Client's bound method :meth:`~pyrogram.Client.run`.

    Parameters:
        clients (List of :obj:`~pyrogram.Client`):
            A list of client objects to run.

    Example:
        .. code-block:: python

            import asyncio
            from pyrogram import Client, compose


            async def main():
                app1 = Client("account1")
                app2 = Client("account2")
                app3 = Client("account3")

                ...

                await compose([app1, app2, app3])


            asyncio.run(main())

    """
    for c in clients:
        await c.start()

    await idle()

    for c in clients:
        await c.stop()

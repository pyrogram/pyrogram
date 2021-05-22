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
import inspect

from pyrogram.methods.utilities.idle import idle
from pyrogram.scaffold import Scaffold


class Run(Scaffold):
    def run(self, coroutine=None):
        """Start the client, idle the main script and finally stop the client.

        This is a convenience method that calls :meth:`~pyrogram.Client.start`, :meth:`~pyrogram.idle` and
        :meth:`~pyrogram.Client.stop` in sequence. It makes running a client less verbose, but is not suitable in case
        you want to run more than one client in a single main script, since :meth:`~pyrogram.idle` will block after
        starting the own client.

        Raises:
            ConnectionError: In case you try to run an already started client.

        Example:
            .. code-block:: python
                :emphasize-lines: 7

                from pyrogram import Client

                app = Client("my_account")

                ...  # Set handlers up

                app.run()
        """
        loop = asyncio.get_event_loop()
        run = loop.run_until_complete

        if coroutine is not None:
            run(coroutine)
        else:
            if inspect.iscoroutinefunction(self.start):
                run(self.start())
                run(idle())
                run(self.stop())
            else:
                self.start()
                run(idle())
                self.stop()

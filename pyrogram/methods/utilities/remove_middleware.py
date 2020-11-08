#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

from pyrogram.middleware import Middleware
from pyrogram.scaffold import Scaffold


class RemoveMiddleware(Scaffold):
    def remove_middleware(self, middleware: "Middleware"):
        """Remove a previously-registered middleware.

        Parameters:
            middleware (``Middleware``):
                The middleware to be removed.

        Example:
            .. code-block:: python
                :emphasize-lines: 10

                from pyrogram import Client

                async def my_middleware(client, update, call_next):
                    print("Before all handlers")
                    await call_next(client, update)
                    print("After all handlers")

                app = Client("my_account")

                app.add_middleware(my_middleware)

                app.remove_middleware(middleware)

                app.run()
        """
        self.dispatcher.remove_middleware(middleware)

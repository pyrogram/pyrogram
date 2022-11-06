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

from typing import Callable

import pyrogram


class Middleware:
    def middleware(self: "pyrogram.Client", func: Callable) -> Callable:
        """Decorator for add middleware.

        This does the same thing as :meth:`~pyrogram.Client.add_middleware`

        Returns:
            ``Middleware``: A callable middleware.

        Example:
            .. code-block:: python
                :emphasize-lines: 9

                from pyrogram import Client

                app = Client("my_account")

                @app.middleware
                async def my_middleware(client, update, call_next):
                    print("Before all handlers")
                    await call_next(client, update)
                    print("After all handlers")

                app.run()

        """
        self.add_middleware(func)
        return func

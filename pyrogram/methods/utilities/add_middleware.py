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

import pyrogram


class AddMiddleware:
    def add_middleware(self: "pyrogram.Client", middleware: "pyrogram.middleware.Middleware"):
        """Register a middleware.

        You can register multiple middlewares, they would be called in order you've added them.
        It is useful for assigning some context variables, like I18n locale or some info about user from your database and so on

        !Note that "call_next" argument must be always called "call_next" and will be passed to your middleware as kwarg

        Parameters:
            middleware (``Middleware``):
                The handler to be registered.

        Returns:
            ``Middleware``: A callable middleware.

        Example:
            .. code-block:: python
                :emphasize-lines: 9

                from pyrogram import Client

                async def my_middleware(client, update, call_next):
                    print("Before all handlers")
                    await call_next(client, update)
                    print("After all handlers")

                app = Client("my_account")

                app.add_middleware(my_middleware)

                app.run()
        """
        self.dispatcher.add_middleware(middleware)
        return middleware

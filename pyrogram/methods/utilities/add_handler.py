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

from pyrogram.handlers import DisconnectHandler
from pyrogram.handlers.handler import Handler
from pyrogram.scaffold import Scaffold


class AddHandler(Scaffold):
    def add_handler(self, handler: "Handler", group: int = 0):
        """Register an update handler.

        You can register multiple handlers, but at most one handler within a group will be used for a single update.
        To handle the same update more than once, register your handler using a different group id (lower group id
        == higher priority). This mechanism is explained in greater details at
        :doc:`More on Updates <../../topics/more-on-updates>`.

        Parameters:
            handler (``Handler``):
                The handler to be registered.

            group (``int``, *optional*):
                The group identifier, defaults to 0.

        Returns:
            ``tuple``: A tuple consisting of *(handler, group)*.

        Example:
            .. code-block:: python

                from pyrogram import Client
                from pyrogram.handlers import MessageHandler

                def dump(client, message):
                    print(message)

                app = Client("my_account")

                app.add_handler(MessageHandler(dump))

                app.run()
        """
        if isinstance(handler, DisconnectHandler):
            self.disconnect_handler = handler.callback
        else:
            self.dispatcher.add_handler(handler, group)

        return handler, group

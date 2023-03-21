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
from typing import Callable
import pyrogram
from .handler import Handler


class ErrorHandler(Handler):
    """The Error handler class. Used to handle errors.
    It is intended to be used with :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_message` decorator.

    Parameters:
        callback (``Callable``):
            Pass a function that will be called when a new Error arrives. It takes *(client, error)*
            as positional arguments (look at the section below for a detailed description).

        errors (:obj:`Exception` | List of :obj:`Exception`):
            Pass one or more exception classes to allow only a subset of errors to be passed
            in your callback function.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the message handler.

        error (:obj:`~Exception`):
            The error that was raised.
    """

    def __init__(self, callback: Callable, errors=None):
        if errors is None:
            errors = [Exception]
        else:
            if not isinstance(errors, list):
                errors = [errors]

        self.errors = errors
        super().__init__(callback)

    async def check(self, client: "pyrogram.Client", error: Exception):
        return any(isinstance(error, e) for e in self.errors)

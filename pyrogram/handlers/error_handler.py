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

import sys
import asyncio

from pyrogram import errors


class ErrorHandler:
    """The Error handler class. Used to handle errors which coming from Telegram server - RPCError and python exceptions
    which inherits from BaseException as well. It is intended to be used with :meth:`~pyrogram.Client.add_handler`

    For a nicer way to register this handler, have a look at the
    :meth:`~pyrogram.Client.on_error` decorator.

    Parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself

        catch_all (`bool`, *optional*):
            This tells whether to catch python exceptions as well or not.

    Other parameters:
        client (:obj:`~pyrogram.Client`):
            The Client itself, useful when you want to call other API methods inside the error handler.

        exception (:obj:`BaseException`):
            The raised exception itself.

    """

    original_run_in_executor = asyncio.BaseEventLoop.run_in_executor
    original_except_hook = sys.excepthook

    def __init__(self, client, callback: callable, catch_all: bool = False):
        self.client = client
        self.callback = callback
        self.exceptions_to_catch = [errors.RPCError]

        if catch_all:
            self.exceptions_to_catch.append(BaseException)
            sys.excepthook = self.except_hook

        asyncio.BaseEventLoop.run_in_executor = self.run_in_executor

    async def run_in_executor(self, *args, **kwargs):
        try:
            result = await self.original_run_in_executor(*args, **kwargs)
        except self.exceptions_to_catch as exc:
            self.callback(self.client, exc[1])
        else:
            return result

    def except_hook(self, *args):
        try:
            self.callback(self.client, args[1])
        except BaseException:
            self.original_except_hook(*sys.exc_info())

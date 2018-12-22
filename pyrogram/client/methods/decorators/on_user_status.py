# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Tuple

import pyrogram
from pyrogram.client.filters.filter import Filter
from pyrogram.client.handlers.handler import Handler
from ...ext import BaseClient


class OnUserStatus(BaseClient):
    def on_user_status(self=None,
                       filters=None,
                       group: int = 0) -> callable:
        """Use this decorator to automatically register a function for handling
        user status updates. This does the same thing as :meth:`add_handler` using the
        :class:`UserStatusHandler`.

        .. note::
            This decorator will wrap your defined function in a tuple consisting of *(Handler, group)*.

            To reference your own function after it has been decorated, you need to access
            *my_function[0].callback*, that is, the *callback* field of Handler object which is the the
            first element in the tuple.

        Args:
            filters (:obj:`Filters <pyrogram.Filters>`):
                Pass one or more filters to allow only a subset of UserStatus updated to be passed in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: callable) -> Tuple[Handler, int]:
            if isinstance(func, tuple):
                func = func[0].callback

            handler = pyrogram.UserStatusHandler(func, filters)

            if isinstance(self, Filter):
                return pyrogram.UserStatusHandler(func, self), group if filters is None else filters

            if self is not None:
                self.add_handler(handler, group)

            return handler, group

        return decorator

# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

from typing import Callable

import pyrogram
from pyrogram.client.filters.filter import Filter
from ...ext import BaseClient


class OnPoll(BaseClient):
    def on_poll(
        self=None,
        filters=None,
        group: int = 0
    ) -> callable:
        """Decorator for handling poll updates.

        This does the same thing as :meth:`~pyrogram.Client.add_handler` using the :obj:`~pyrogram.PollHandler`.

        Parameters:
            filters (:obj:`~pyrogram.Filters`, *optional*):
                Pass one or more filters to allow only a subset of polls to be passed
                in your function.

            group (``int``, *optional*):
                The group identifier, defaults to 0.
        """

        def decorator(func: Callable) -> Callable:
            if isinstance(self, pyrogram.Client):
                self.add_handler(pyrogram.PollHandler(func, filters), group)
            elif isinstance(self, Filter) or self is None:
                func.handler = (
                    pyrogram.PollHandler(func, self),
                    group if filters is None else filters
                )

            return func

        return decorator

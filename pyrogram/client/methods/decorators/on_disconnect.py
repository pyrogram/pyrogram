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

import pyrogram
from ...ext import BaseClient


class OnDisconnect(BaseClient):
    def on_disconnect(self):
        """Use this decorator to automatically register a function for handling
        disconnections. This does the same thing as :meth:`add_handler` using the
        :class:`DisconnectHandler`.
        """

        def decorator(func):
            self.add_handler(pyrogram.DisconnectHandler(func))
            return func

        return decorator

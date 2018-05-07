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

from pyrogram.api import functions, types
from ...ext import BaseClient, utils


class GetMe(BaseClient):
    def get_me(self):
        """A simple method for testing your authorization. Requires no parameters.

        Returns:
            Basic information about the user or bot in form of a :obj:`User` object

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        return utils.parse_user(
            self.send(
                functions.users.GetFullUser(
                    types.InputPeerSelf()
                )
            ).user
        )

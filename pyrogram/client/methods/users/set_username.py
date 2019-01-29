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

from pyrogram.api import functions
from ...ext import BaseClient


class SetUsername(BaseClient):
    def set_username(self,
                     username: str) -> bool:
        """Use this method to set a username.

        This method only works for Users.
        Bots usernames must be changed via Telegram Support.

        Args:
            username (``str``):
                Username to set.

        Returns:
            True on success.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """

        return bool(
            self.send(
                functions.account.UpdateUsername(username)
            )
        )

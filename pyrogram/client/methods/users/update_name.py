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


class UpdateName(BaseClient):
    def update_name(
        self,
        first_name: str,
        last_name: str = None
    ) -> bool:
        """Update your own name.

        This method only works for users, not bots. Bot name must be changed via BotFather.

        Parameters:
            first_name (``str``):
                first_name to set.

            last_name (``str``, *optional*):
                last_name to set. "" (empty string) or None to remove it.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                app.update_name(first_name="Dan", last_name="")
        """

        return bool(
            self.send(
                functions.account.UpdateProfile(
                    first_name=first_name,
                    last_name=last_name or "",
                )
            )
        )


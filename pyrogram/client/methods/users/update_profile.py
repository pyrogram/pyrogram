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


class UpdateProfile(BaseClient):
    def set_profile_photo(
        self,
        first_name: str = None,
        last_name: str = None,
        about: str = None
    ) -> bool:
        """Update your pofile.
        Parameters:
            first_name (``str``):
                The new first name.
                Pass the first name as string.
            last_name (``str``):
                The new last name.
                Pass the last name as string.
            about (``str``):
                The new about.
                Pass the about as string. 70 characters max.
        Returns:
            ``bool``: True on success.
        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return bool(
            self.send(
                functions.account.UpdateProfile(
                    first_name=self.first_name,
                    last_name=self.last_name,
                    about=self.about
                )
            )
        )

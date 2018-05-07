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

from hashlib import sha256

from pyrogram.api import functions, types
from ...ext import BaseClient


class RemoveCloudPassword(BaseClient):
    def remove_cloud_password(self, password: str):
        """Use this method to turn off the Two-Step Verification security feature (Cloud Password) on your account.

        Args:
            password (``str``):
                Your current password.

        Returns:
            True on success, False otherwise.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        r = self.send(functions.account.GetPassword())

        if isinstance(r, types.account.Password):
            password_hash = sha256(r.current_salt + password.encode() + r.current_salt).digest()

            return self.send(
                functions.account.UpdatePasswordSettings(
                    current_password_hash=password_hash,
                    new_settings=types.account.PasswordInputSettings(
                        new_salt=b"",
                        new_password_hash=b"",
                        hint=""
                    )
                )
            )
        else:
            return False

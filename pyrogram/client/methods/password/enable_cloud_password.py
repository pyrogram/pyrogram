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

import os
from hashlib import sha256

from pyrogram.api import functions, types
from ...ext import BaseClient


class EnableCloudPassword(BaseClient):
    def enable_cloud_password(self, password: str, hint: str = "", email: str = ""):
        """Use this method to enable the Two-Step Verification security feature (Cloud Password) on your account.

        This password will be asked when you log in on a new device in addition to the SMS code.

        Args:
            password (``str``):
                Your password.

            hint (``str``, *optional*):
                A password hint.

            email (``str``, *optional*):
                Recovery e-mail.

        Returns:
            True on success, False otherwise.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        r = self.send(functions.account.GetPassword())

        if isinstance(r, types.account.NoPassword):
            salt = r.new_salt + os.urandom(8)
            password_hash = sha256(salt + password.encode() + salt).digest()

            return self.send(
                functions.account.UpdatePasswordSettings(
                    current_password_hash=salt,
                    new_settings=types.account.PasswordInputSettings(
                        new_salt=salt,
                        new_password_hash=password_hash,
                        hint=hint,
                        email=email
                    )
                )
            )
        else:
            return False

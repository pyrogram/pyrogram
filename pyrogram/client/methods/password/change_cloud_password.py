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


class ChangeCloudPassword(BaseClient):
    def change_cloud_password(self, current_password: str, new_password: str, new_hint: str = ""):
        """Use this method to change your Two-Step Verification password (Cloud Password) with a new one.

        Args:
            current_password (``str``):
                Your current password.

            new_password (``str``):
                Your new password.

            new_hint (``str``, *optional*):
                A new password hint.

        Returns:
            True on success, False otherwise.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        r = self.send(functions.account.GetPassword())

        if isinstance(r, types.account.Password):
            current_password_hash = sha256(r.current_salt + current_password.encode() + r.current_salt).digest()

            new_salt = r.new_salt + os.urandom(8)
            new_password_hash = sha256(new_salt + new_password.encode() + new_salt).digest()

            return self.send(
                functions.account.UpdatePasswordSettings(
                    current_password_hash=current_password_hash,
                    new_settings=types.account.PasswordInputSettings(
                        new_salt=new_salt,
                        new_password_hash=new_password_hash,
                        hint=new_hint
                    )
                )
            )
        else:
            return False

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

from pyrogram.api import functions, types
from .utils import compute_check
from ...ext import BaseClient


class RemoveCloudPassword(BaseClient):
    async def remove_cloud_password(
        self,
        password: str
    ) -> bool:
        """Turn off the Two-Step Verification security feature (Cloud Password) on your account.

        Parameters:
            password (``str``):
                Your current password.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is no cloud password to remove.

        Example:
            .. code-block:: python

                app.remove_cloud_password("password")
        """
        r = await self.send(functions.account.GetPassword())

        if not r.has_password:
            raise ValueError("There is no cloud password to remove")

        await self.send(
            functions.account.UpdatePasswordSettings(
                password=compute_check(r, password),
                new_settings=types.account.PasswordInputSettings(
                    new_algo=types.PasswordKdfAlgoUnknown(),
                    new_password_hash=b"",
                    hint=""
                )
            )
        )

        return True

#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

import os

from pyrogram import raw
from pyrogram.scaffold import Scaffold
from pyrogram.utils import compute_password_hash, btoi, itob


class EnableCloudPassword(Scaffold):
    async def enable_cloud_password(
        self,
        password: str,
        hint: str = "",
        email: str = None
    ) -> bool:
        """Enable the Two-Step Verification security feature (Cloud Password) on your account.

        This password will be asked when you log-in on a new device in addition to the SMS code.

        Parameters:
            password (``str``):
                Your password.

            hint (``str``, *optional*):
                A password hint.

            email (``str``, *optional*):
                Recovery e-mail.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is already a cloud password enabled.

        Example:
            .. code-block:: python

                # Enable password without hint and email
                app.enable_cloud_password("password")

                # Enable password with hint and without email
                app.enable_cloud_password("password", hint="hint")

                # Enable password with hint and email
                app.enable_cloud_password("password", hint="hint", email="user@email.com")
        """
        r = await self.send(raw.functions.account.GetPassword())

        if r.has_password:
            raise ValueError("There is already a cloud password enabled")

        r.new_algo.salt1 += os.urandom(32)
        new_hash = btoi(compute_password_hash(r.new_algo, password))
        new_hash = itob(pow(r.new_algo.g, new_hash, btoi(r.new_algo.p)))

        await self.send(
            raw.functions.account.UpdatePasswordSettings(
                password=raw.types.InputCheckPasswordEmpty(),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=r.new_algo,
                    new_password_hash=new_hash,
                    hint=hint,
                    email=email
                )
            )
        )

        return True

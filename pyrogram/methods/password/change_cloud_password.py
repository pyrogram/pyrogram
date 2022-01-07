#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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
from pyrogram.utils import compute_password_hash, compute_password_check, btoi, itob


class ChangeCloudPassword(Scaffold):
    async def change_cloud_password(
        self,
        current_password: str,
        new_password: str,
        new_hint: str = ""
    ) -> bool:
        """Change your Two-Step Verification password (Cloud Password) with a new one.

        Parameters:
            current_password (``str``):
                Your current password.

            new_password (``str``):
                Your new password.

            new_hint (``str``, *optional*):
                A new password hint.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: In case there is no cloud password to change.

        Example:
            .. code-block:: python

                # Change password only
                app.change_cloud_password("current_password", "new_password")

                # Change password and hint
                app.change_cloud_password("current_password", "new_password", new_hint="hint")
        """
        r = await self.send(raw.functions.account.GetPassword())

        if not r.has_password:
            raise ValueError("There is no cloud password to change")

        r.new_algo.salt1 += os.urandom(32)
        new_hash = btoi(compute_password_hash(r.new_algo, new_password))
        new_hash = itob(pow(r.new_algo.g, new_hash, btoi(r.new_algo.p)))

        await self.send(
            raw.functions.account.UpdatePasswordSettings(
                password=compute_password_check(r, current_password),
                new_settings=raw.types.account.PasswordInputSettings(
                    new_algo=r.new_algo,
                    new_password_hash=new_hash,
                    hint=new_hint
                )
            )
        )

        return True

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

from pyrogram import raw
from pyrogram.scaffold import Scaffold

class DeleteAccount(Scaffold):
    def delete_account(
        self,
        reason: str = None
    ) -> bool:
        """Delete your own account.
        
        :meth:`~Client.delete_account`.

        Parameters:
            reason (``str`` | ``None``):
            reason to set. "" (empty string) or None to remove it.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                app.delete_account(reason="forgot password")
        """

        return bool(
            await self.send(
                raw.functions.account.DeleteAccount(
                    reason=reason
                )
            )
        )

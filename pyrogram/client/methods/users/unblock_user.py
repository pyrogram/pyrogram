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

from typing import Union

from pyrogram.api import functions

from ...ext import BaseClient


class UnblockUser(BaseClient):
    async def unblock_user(
        self,
        user_id: Union[int, str]
    ) -> bool:
        """Unblock a user.

        Returns:
            ``bool``: True on success

        Raises:
            RPCError: In case of Telegram RPC Error.
        """
        return bool(
            await self.send(
                functions.contact.Unblock(
                    id=await self.resolve_peer(user_id)
                )
            )
        )

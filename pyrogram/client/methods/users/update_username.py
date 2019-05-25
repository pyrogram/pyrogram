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


class UpdateUsername(BaseClient):
    async def update_username(
        self,
        username: Union[str, None]
    ) -> bool:
        """Update your own username.
        
        This method only works for users, not bots. Bot usernames must be changed via Bot Support or by recreating
        them from scratch using BotFather. To update a channel or supergroup username you can use
        :meth:`update_chat_username`.

        Parameters:
            username (``str`` | ``None``):
                Username to set. "" (empty string) or None to remove it.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return bool(
            await self.send(
                functions.account.UpdateUsername(
                    username=username or ""
                )
            )
        )

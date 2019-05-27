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

from pyrogram.api import functions, types

from ...ext import BaseClient


class GetUserDC(BaseClient):
    def get_user_dc(self, user_id: Union[int, str]) -> Union[int, None]:
        """Get the assigned data center (DC) of a user.

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            ``int`` | ``None``: The DC identifier as integer, or None in case it wasn't possible to get it.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        r = self.send(functions.users.GetUsers(id=[self.resolve_peer(user_id)]))

        if r:
            r = r[0]

            if r.photo:
                if isinstance(r.photo.photo_small, types.FileLocation):
                    return r.photo.photo_small.dc_id

        return None

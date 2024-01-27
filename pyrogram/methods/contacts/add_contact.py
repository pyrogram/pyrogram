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

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram import types


class AddContact:
    async def add_contact(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        first_name: str,
        last_name: str = "",
        phone_number: str = "",
        share_phone_number: bool = False
    ):
        """Add an existing Telegram user as contact, even without a phone number.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.

            first_name (``str``):
                User's first name.

            last_name (``str``, *optional*):
                User's last name.

            phone_number (``str``, *optional*):
                User's phone number.

            share_phone_number (``bool``, *optional*):
                Whether or not to share the phone number with the user.
                Defaults to False.

        Returns:
            :obj:`~pyrogram.types.User`: On success the user is returned.

        Example:
            .. code-block:: python

                # Add contact by id
                await app.add_contact(12345678, "Foo")

                # Add contact by username
                await app.add_contact("username", "Bar")
        """
        r = await self.invoke(
            raw.functions.contacts.AddContact(
                id=await self.resolve_peer(user_id),
                first_name=first_name,
                last_name=last_name,
                phone=phone_number,
                add_phone_privacy_exception=share_phone_number
            )
        )

        return types.User._parse(self, r.users[0])

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

import logging
from typing import List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold

log = logging.getLogger(__name__)


class GetContacts(Scaffold):
    async def get_contacts(self) -> List["types.User"]:
        """Get contacts from your Telegram address book.

        Returns:
            List of :obj:`~pyrogram.types.User`: On success, a list of users is returned.

        Example:
            .. code-block:: python

                contacts = app.get_contacts()
                print(contacts)
        """
        contacts = await self.send(raw.functions.contacts.GetContacts(hash=0))
        return types.List(types.User._parse(self, user) for user in contacts.users)

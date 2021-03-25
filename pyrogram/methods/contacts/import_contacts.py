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

from typing import List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class ImportContacts(Scaffold):
    async def import_contacts(
        self,
        contacts: List["types.InputPhoneContact"]
    ):
        """Import contacts to your Telegram address book.

        Parameters:
            contacts (List of :obj:`~pyrogram.types.InputPhoneContact`):
                The contact list to be added

        Returns:
            :obj:`types.contacts.ImportedContacts`

        Example:
            .. code-block:: python

                from pyrogram.types import InputPhoneContact

                app.import_contacts([
                    InputPhoneContact("39123456789", "Foo"),
                    InputPhoneContact("38987654321", "Bar"),
                    InputPhoneContact("01234567891", "Baz")])
        """
        imported_contacts = await self.send(
            raw.functions.contacts.ImportContacts(
                contacts=contacts
            )
        )

        return imported_contacts

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
from pyrogram.errors import PeerIdInvalid
from pyrogram.scaffold import Scaffold


class DeleteContacts(Scaffold):
    async def delete_contacts(
        self,
        ids: List[int]
    ):
        """Delete contacts from your Telegram address book.

        Parameters:
            ids (List of ``int``):
                A list of unique identifiers for the target users.
                Can be an ID (int), a username (string) or phone number (string).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                app.delete_contacts([user_id1, user_id2, user_id3])
        """
        contacts = []

        for i in ids:
            try:
                input_user = await self.resolve_peer(i)
            except PeerIdInvalid:
                continue
            else:
                if isinstance(input_user, raw.types.InputPeerUser):
                    contacts.append(input_user)

        return await self.send(
            raw.functions.contacts.DeleteContacts(
                id=contacts
            )
        )

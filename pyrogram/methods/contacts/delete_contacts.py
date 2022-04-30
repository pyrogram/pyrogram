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

from typing import List, Union

import pyrogram
from pyrogram import raw, types


class DeleteContacts:
    async def delete_contacts(
        self: "pyrogram.Client",
        user_ids: Union[int, str, List[Union[int, str]]]
    ) -> Union["types.User", List["types.User"], None]:
        """Delete contacts from your Telegram address book.

        Parameters:
            user_ids (``int`` | ``str`` | List of ``int`` or ``str``):
                A single user id/username o a list of user identifiers (id or username).

        Returns:
            :obj:`~pyrogram.types.User` | List of :obj:`~pyrogram.types.User` | ``None``: In case *user_ids* was an
            integer or a string, a single User object is returned. In case *user_ids* was a list, a list of User objects
            is returned. In case nothing changed after calling the method (for example, when deleting a non-existent
            contact), None is returned.

        Example:
            .. code-block:: python

                await app.delete_contacts(user_id)
                await app.delete_contacts([user_id1, user_id2, user_id3])
        """
        is_list = isinstance(user_ids, list)

        if not is_list:
            user_ids = [user_ids]

        r = await self.invoke(
            raw.functions.contacts.DeleteContacts(
                id=[await self.resolve_peer(i) for i in user_ids]
            )
        )

        if not r.updates:
            return None

        users = types.List([types.User._parse(self, i) for i in r.users])

        return users if is_list else users[0]

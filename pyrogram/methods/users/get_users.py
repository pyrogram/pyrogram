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

import asyncio
from typing import Iterable, Union, List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class GetUsers(Scaffold):
    async def get_users(
        self,
        user_ids: Union[Iterable[Union[int, str]], int, str]
    ) -> Union["types.User", List["types.User"]]:
        """Get information about a user.
        You can retrieve up to 200 users at once.

        Parameters:
            user_ids (``iterable``):
                A list of User identifiers (id or username) or a single user id/username.
                For a contact that exists in your Telegram address book you can use his phone number (str).
                Iterators and Generators are also accepted.

        Returns:
            :obj:`~pyrogram.types.User` | List of :obj:`~pyrogram.types.User`: In case *user_ids* was an integer or
            string the single requested user is returned, otherwise, in case *user_ids* was an iterable a list of users
            is returned, even if the iterable contained one item only.

        Example:
            .. code-block:: python

                # Get information about one user
                app.get_users("me")

                # Get information about multiple users at once
                app.get_users([user1, user2, user3])
        """
        is_iterable = not isinstance(user_ids, (int, str))
        user_ids = list(user_ids) if is_iterable else [user_ids]
        user_ids = await asyncio.gather(*[self.resolve_peer(i) for i in user_ids])

        r = await self.send(
            raw.functions.users.GetUsers(
                id=user_ids
            )
        )

        users = types.List()

        for i in r:
            users.append(types.User._parse(self, i))

        return users if is_iterable else users[0]

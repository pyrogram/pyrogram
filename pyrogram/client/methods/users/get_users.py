# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

from pyrogram.api import functions
from ...ext import BaseClient, utils


class GetUsers(BaseClient):
    def get_users(self, user_ids):
        """Use this method to get information about a user.
        You can retrieve up to 200 users at once.

        Args:
            user_ids (``iterable``):
                A list of User identifiers (id or username) or a single user id/username.
                For a contact that exists in your Telegram address book you can use his phone number (str).
                Iterators and Generators are also accepted.

        Returns:
            On success and in case *user_ids* was a list, the returned value will be a list of the requested
            :obj:`Users <User>` even if a list contains just one element, otherwise if
            *user_ids* was an integer, the single requested :obj:`User` is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        is_iterable = not isinstance(user_ids, (int, str))
        user_ids = list(user_ids) if is_iterable else [user_ids]
        user_ids = [self.resolve_peer(i) for i in user_ids]

        r = self.send(
            functions.users.GetUsers(
                id=user_ids
            )
        )

        users = []

        for i in r:
            users.append(utils.parse_user(i))

        return users if is_iterable else users[0]

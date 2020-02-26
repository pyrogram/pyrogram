# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

import pyrogram
from ..object import Object


class PollOptionVote(Object):
    """Contains vote info for an option in a public poll.

    Parameters:
        user (``pyrogram.User``):
            Voter object.

        date (``int``):
            Date the vote was submitted in Unix time.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.BaseClient" = None,
        user: 'pyrogram.User',
        date: int
    ):
        super().__init__(client)

        self.user = user
        self.date = date

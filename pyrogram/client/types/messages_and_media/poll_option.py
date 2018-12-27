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

import pyrogram
from ..pyrogram_type import PyrogramType


class PollOption(PyrogramType):
    """This object represents a Poll Option.

    Args:
        text (``str``):
            Text of the poll option.

        voters (``int``):
            The number of users who voted this option.

        data (``bytes``):
            Unique data that identifies this option among all the other options in a poll.
    """

    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 text: str,
                 voters: int,
                 data: bytes):
        super().__init__(client)

        self.text = text
        self.voters = voters
        self.data = data

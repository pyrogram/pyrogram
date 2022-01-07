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

import pyrogram
from ..object import Object


class Reaction(Object):
    """Contains information about a reaction.

    Parameters:
        emoji (``str``):
            Reaction emoji.

        count (``int``):
            Reaction count.

        chosen (``bool``):
            Whether this is the chosen reaction.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        emoji: str,
        count: int,
        chosen: bool
    ):
        super().__init__(client)

        self.emoji = emoji
        self.count = count
        self.chosen = chosen

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

from ..object import Object


class RequestPeerTypeUserInfo(Object):
    """Contains information about a user peer type.

    Parameters:
        is_bot (``bool``):
            If True, returns the list of users where user is a bot.

        is_premium (``bool``):
            If True, returns the list of users where user has premium.
    """

    def __init__(
        self, *,
        is_bot: bool = None,
        is_premium: bool = None,
    ):
        super().__init__()

        self.is_bot = is_bot
        self.is_premium = is_premium

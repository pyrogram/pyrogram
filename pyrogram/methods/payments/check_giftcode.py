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
import re

import pyrogram
from pyrogram import raw, types


class CheckGiftCode:
    async def check_gift_code(
        self: "pyrogram.Client",
        link: str,
    ) -> "types.CheckedGiftCode":
        """Get information about a gift code.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            link (``str``):
                The gift code link.

        Returns:
            :obj:`~pyrogram.types.CheckedGiftCode`: On success, a checked gift code is returned.

        Raises:
            ValueError: In case the folder invite link is invalid.

        Example:
            .. code-block:: python

                # get information about a gift code
                app.check_gift_code("t.me/giftcode/abc1234567def")
        """
        match = re.match(r"^(?:https?://)?(?:www\.)?(?:t(?:elegram)?\.(?:org|me|dog)/(?:giftcode/|\+))([\w-]+)$", link)

        if match:
            slug = match.group(1)
        elif isinstance(link, str):
            slug = link
        else:
            raise ValueError("Invalid gift code link")

        r = await self.invoke(
            raw.functions.payments.CheckGiftCode(
                slug=slug
            )
        )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}

        return types.CheckedGiftCode._parse(self, r, users, chats)

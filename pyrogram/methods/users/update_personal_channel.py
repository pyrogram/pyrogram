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

from typing import Union

import pyrogram
from pyrogram import raw


class UpdatePersonalChannel:
    async def update_personal_channel(
        self: "pyrogram.Client",
        chat_id: Union[int, str] = None
    ) -> bool:
        """Update your personal channel.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                Use :meth:`~pyrogram.Client.get_personal_channels` to get available channels.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Update your personal channel
                await app.update_personal_channel(chat_id)

                # Remove personal channel from your profile
                await app.update_personal_channel()
        """
        if chat_id is None:
            peer = raw.types.InputChannelEmpty()
        else:
            peer = await self.resolve_peer(chat_id)

            if not isinstance(peer, raw.types.InputChannel):
                return False

        return bool(
            await self.invoke(
                raw.functions.account.UpdatePersonalChannel(
                    channel=peer
                )
            )
        )

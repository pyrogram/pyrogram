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
from pyrogram import types


class StartBot:
    async def start_bot(
        self: "pyrogram.Client",
        bot: Union[int, str],
        start_param: str = ""
    ) -> bool:
        """Start bot

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            bot (``int`` | ``str``):
                Unique identifier of the bot you want to be started. You can specify
                a @username (str) or a bot ID (int).

            start_param (``str``):
                Text of the param (up to 64 characters).
                Defaults to "" (empty string).

        Returns:
            ``bool`` - On success, True is returned.

        Example:
            .. code-block:: python

                # Start bot
                await app.start_bot("pyrogrambot")
        """
        r = await self.invoke(
            raw.functions.messages.StartBot(
                bot=await self.resolve_peer(bot),
                peer=raw.types.InputPeerSelf(),
                random_id=self.rnd_id(),
                start_param=start_param
            )
        )

        for i in r.updates:
            if isinstance(i, raw.types.UpdateNewMessage):
                return await types.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

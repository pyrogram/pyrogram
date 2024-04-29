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

import logging
from typing import Union, List

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils

log = logging.getLogger(__name__)


class GetScheduledMessages:
    async def get_scheduled_messages(
        self: "pyrogram.Client",
        chat_id: Union[int, str]
    ) -> List["types.Message"]:
        """Get one or more scheduled messages from a chat.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            :List of :obj:`~pyrogram.types.Message`: a list of messages is returned.

        Example:
            .. code-block:: python

                # Get scheduled messages
                await app.get_scheduled_messages(chat_id)

        Raises:
            ValueError: In case of invalid arguments.
        """
        r = await self.invoke(
            raw.functions.messages.GetScheduledHistory(peer=await self.resolve_peer(chat_id), hash=0)
        )

        return await utils.parse_messages(self, r, replies=0)

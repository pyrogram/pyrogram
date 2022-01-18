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

from pyrogram import raw
from pyrogram.scaffold import Scaffold


class SendReaction(Scaffold):
    async def send_reaction(
        self,
        chat_id: Union[int, str],
        message_id: int,
        emoji: str = ""
    ) -> bool:
        """Send a reaction to a message.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Identifier of the message.

            emoji (``str``, *optional*):
                Reaction emoji.
                Pass "" as emoji (default) to retract the reaction.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Send a reaction
                app.send_reaction(chat_id, message_id, "🔥")

                # Retract a reaction
                app.send_reaction(chat_id, message_id)
        """
        await self.send(
            raw.functions.messages.SendReaction(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                reaction=emoji
            )
        )

        return True

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

from typing import Union, List

import pyrogram
from pyrogram import raw
from pyrogram import types


class GetGameHighScores:
    async def get_game_high_scores(
        self: "pyrogram.Client",
        user_id: Union[int, str],
        chat_id: Union[int, str],
        message_id: int = None
    ) -> List["types.GameHighScore"]:
        """Get data for high score tables.

        Parameters:
            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            chat_id (``int`` | ``str``, *optional*):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                Required if inline_message_id is not specified.

            message_id (``int``, *optional*):
                Identifier of the sent message.
                Required if inline_message_id is not specified.

        Returns:
            List of :obj:`~pyrogram.types.GameHighScore`: On success.

        Example:
            .. code-block:: python

                scores = await app.get_game_high_scores(user_id, chat_id, message_id)
                print(scores)
        """
        # TODO: inline_message_id

        r = await self.invoke(
            raw.functions.messages.GetGameHighScores(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                user_id=await self.resolve_peer(user_id)
            )
        )

        return types.List(types.GameHighScore._parse(self, score, r.users) for score in r.scores)

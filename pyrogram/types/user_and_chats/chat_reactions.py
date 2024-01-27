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

from typing import Optional, List

import pyrogram
from pyrogram import raw, types
from ..object import Object


class ChatReactions(Object):
    """A chat reactions

    Parameters:
        all_are_enabled (``bool``, *optional*)

        allow_custom_emoji (``bool``, *optional*):
            Whether custom emoji are allowed or not.

        reactions (List of :obj:`~pyrogram.types.Reaction`, *optional*):
            Reactions available.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        all_are_enabled: Optional[bool] = None,
        allow_custom_emoji: Optional[bool] = None,
        reactions: Optional[List["types.Reaction"]] = None,
    ):
        super().__init__(client)

        self.all_are_enabled = all_are_enabled
        self.allow_custom_emoji = allow_custom_emoji
        self.reactions = reactions

    @staticmethod
    def _parse(client, chat_reactions: "raw.base.ChatReactions") -> Optional["ChatReactions"]:
        if isinstance(chat_reactions, raw.types.ChatReactionsAll):
            return ChatReactions(
                client=client,
                all_are_enabled=True,
                allow_custom_emoji=chat_reactions.allow_custom
            )

        if isinstance(chat_reactions, raw.types.ChatReactionsSome):
            return ChatReactions(
                client=client,
                reactions=[types.Reaction._parse(client, reaction)
                           for reaction in chat_reactions.reactions]
            )

        return None

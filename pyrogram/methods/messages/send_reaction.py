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


class SendReaction:
    async def send_reaction(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int = None,
        emoji: Union[int, str, List[Union[int, str]]] = None,
        story_id: int = None,
        big: bool = False
    ) -> bool:
        """Send a reaction to a message or story.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``, *optional*):
                Identifier of the message.

            emoji (``int`` | ``str`` | List of ``int`` | ``str``, *optional*):
                Reaction emoji.
                Pass None as emoji (default) to retract the reaction.
                Pass list of int or str to react multiple emojis.

            story_id (``int``, *optional*):
                Identifier of the story.

            big (``bool``, *optional*):
                Pass True to show a bigger and longer reaction.
                Defaults to False.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Send a reaction
                await app.send_reaction(chat_id, message_id=message_id, emoji="🔥")

                # Send a multiple reactions
                await app.send_reaction(chat_id, message_id=message_id, emoji=["🔥", "❤️"])

                # Send a reaction with premium emoji
                await app.send_reaction(chat_id, message_id=message_id, emoji=5319161050128459957)

                # Send a reaction to story
                await app.send_reaction(chat_id, story_id=story_id, emoji="❤️")

                # Retract a reaction
                await app.send_reaction(chat_id, message_id=message_id)
        """
        if isinstance(emoji, list):
            emoji = [
                    raw.types.ReactionCustomEmoji(document_id=i)
                    if isinstance(i, int)
                    else raw.types.ReactionEmoji(emoticon=i)
                    for i in emoji
            ] if emoji else None
        else:
            if isinstance(emoji, int):
                emoji = [raw.types.ReactionCustomEmoji(document_id=emoji)]
            else:
                emoji = [raw.types.ReactionEmoji(emoticon=emoji)] if emoji else None

        if story_id:
            rpc = raw.functions.stories.SendReaction(
                peer=await self.resolve_peer(chat_id),
                story_id=story_id,
                reaction=emoji[0] if emoji else None,
            )
        else:
            rpc = raw.functions.messages.SendReaction(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                reaction=emoji,
                big=big
            )

        await self.invoke(rpc)

        return True

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
from pyrogram import types
from pyrogram.scaffold import Scaffold


class GetDiscussionMessage(Scaffold):
    async def get_discussion_message(
        self,
        chat_id: Union[int, str],
        message_id: int,
    ) -> "types.Message":
        """Get the discussion message from the linked discussion group of a channel post.

        Reply to the returned message to leave a comment on the linked channel post.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Message id.

        Example:
            .. code-block:: python

                # Get the discussion message
                m = app.get_discussion_message(channel_id, message_id)

                # Comment to the post by replying
                m.reply("comment")
        """
        r = await self.send(
            raw.functions.messages.GetDiscussionMessage(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id
            )
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        return await types.Message._parse(self, r.messages[0], users, chats)

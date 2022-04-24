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


class GetDiscussionMessage:
    async def get_discussion_message(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int,
    ) -> "types.Message":
        """Get the first discussion message of a channel post or a discussion thread in a group.

        Reply to the returned message to leave a comment on the linked channel post or to continue
        the discussion thread.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            message_id (``int``):
                Message id.

        Example:
            .. code-block:: python

                # Get the discussion message
                m = await app.get_discussion_message(channel_id, message_id)

                # Comment to the post by replying
                await m.reply("comment")
        """
        r = await self.invoke(
            raw.functions.messages.GetDiscussionMessage(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id
            )
        )

        users = {u.id: u for u in r.users}
        chats = {c.id: c for c in r.chats}

        return await types.Message._parse(self, r.messages[0], users, chats)

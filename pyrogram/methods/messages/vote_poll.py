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

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class VotePoll(Scaffold):
    async def vote_poll(
        self,
        chat_id: Union[int, str],
        message_id: id,
        options: Union[int, List[int]]
    ) -> "types.Poll":
        """Vote a poll.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Identifier of the original message with the poll.

            options (``Int`` | List of ``int``):
                Index or list of indexes (for multiple answers) of the poll option(s) you want to vote for (0 to 9).

        Returns:
            :obj:`~pyrogram.types.Poll` - On success, the poll with the chosen option is returned.

        Example:
            .. code-block:: python

                app.vote_poll(chat_id, message_id, 6)
        """

        poll = (await self.get_messages(chat_id, message_id)).poll
        options = [options] if not isinstance(options, list) else options

        r = await self.send(
            raw.functions.messages.SendVote(
                peer=await self.resolve_peer(chat_id),
                msg_id=message_id,
                options=[poll.options[option].data for option in options]
            )
        )

        return types.Poll._parse(self, r.updates[0])

# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

from pyrogram.api import functions
from pyrogram.client.ext import BaseClient


class VotePoll(BaseClient):
    def vote_poll(self,
                  chat_id: Union[int, str],
                  message_id: id,
                  option: int) -> bool:
        """Use this method to vote a poll.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Unique poll message identifier inside this chat.

            option (``int``):
                Index of the poll option you want to vote for (0 to 9).

        Returns:
            On success, True is returned.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """
        poll = self.get_messages(chat_id, message_id).poll

        self.send(
            functions.messages.SendVote(
                peer=self.resolve_peer(chat_id),
                msg_id=message_id,
                options=[poll.options[option].data]
            )
        )

        return True

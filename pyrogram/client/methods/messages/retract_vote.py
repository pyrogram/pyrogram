# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

import pyrogram
from pyrogram.api import functions
from pyrogram.client.ext import BaseClient


class RetractVote(BaseClient):
    def retract_vote(
        self,
        chat_id: Union[int, str],
        message_id: int
    ) -> "pyrogram.Poll":
        """Use this method to retract your vote in a poll.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Identifier of the original message with the poll.

        Returns:
            On success, the :obj:`Poll <pyrogram.Poll>` with the retracted vote is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        r = self.send(
            functions.messages.SendVote(
                peer=self.resolve_peer(chat_id),
                msg_id=message_id,
                options=[]
            )
        )

        return pyrogram.Poll._parse(self, r.updates[0])

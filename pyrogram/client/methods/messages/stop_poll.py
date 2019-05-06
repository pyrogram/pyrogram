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
from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient


class StopPoll(BaseClient):
    async def stop_poll(
        self,
        chat_id: Union[int, str],
        message_id: int,
        reply_markup: "pyrogram.InlineKeyboardMarkup" = None
    ) -> "pyrogram.Poll":
        """Use this method to stop a poll which was sent by you.

        Stopped polls can't be reopened and nobody will be able to vote in it anymore.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Identifier of the original message with the poll.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the stopped :obj:`Poll <pyrogram.Poll>` with the final results is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        poll = (await self.get_messages(chat_id, message_id)).poll

        r = await self.send(
            functions.messages.EditMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                media=types.InputMediaPoll(
                    poll=types.Poll(
                        id=poll.id,
                        closed=True,
                        question="",
                        answers=[]
                    )
                ),
                reply_markup=reply_markup.write() if reply_markup else None
            )
        )

        return pyrogram.Poll._parse(self, r.updates[0])

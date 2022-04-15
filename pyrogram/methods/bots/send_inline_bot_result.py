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


class SendInlineBotResult(Scaffold):
    async def send_inline_bot_result(
        self,
        chat_id: Union[int, str],
        query_id: int,
        result_id: str,
        disable_notification: bool = None,
        reply_to_message_id: int = None
    ):
        """Send an inline bot result.
        Bot results can be retrieved using :meth:`~pyrogram.Client.get_inline_bot_results`

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            query_id (``int``):
                Unique identifier for the answered query.

            result_id (``str``):
                Unique identifier for the result that was chosen.

            disable_notification (``bool``, *optional*):
                Sends the message silently.
                Users will receive a notification with no sound.

            reply_to_message_id (``bool``, *optional*):
                If the message is a reply, ID of the original message.

        Returns:
            :obj:`~pyrogram.types.Message`: On success, the sent inline result message is returned.

        Example:
            .. code-block:: python

                app.send_inline_bot_result(chat_id, query_id, result_id)
        """
        return await self.send(
            raw.functions.messages.SendInlineBotResult(
                peer=await self.resolve_peer(chat_id),
                query_id=query_id,
                id=result_id,
                random_id=self.rnd_id(),
                silent=disable_notification or None,
                reply_to_msg_id=reply_to_message_id
            )
        )

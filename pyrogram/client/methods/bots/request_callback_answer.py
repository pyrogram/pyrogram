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

from pyrogram.api import functions
from pyrogram.client.ext import BaseClient


class RequestCallbackAnswer(BaseClient):
    def request_callback_answer(self,
                                chat_id: int or str,
                                message_id: int,
                                callback_data: str):
        """Use this method to request a callback answer from bots. This is the equivalent of clicking an
        inline button containing callback data.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                For a private channel/supergroup you can use its *t.me/joinchat/* link.

            message_id (``int``):
                The message id the inline keyboard is attached on.

            callback_data (``str``):
                Callback data associated with the inline button you want to get the answer from.

        Returns:
            The answer containing info useful for clients to display a notification at the top of the chat screen
            or as an alert.

        Raises:
            :class:`Error <pyrogram.Error>`
            ``TimeoutError``: If the bot fails to answer within 10 seconds
        """
        return self.send(
            functions.messages.GetBotCallbackAnswer(
                peer=self.resolve_peer(chat_id),
                msg_id=message_id,
                data=callback_data.encode()
            ),
            retries=0,
            timeout=10
        )

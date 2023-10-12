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

from pyrogram import raw
from ..object import Object


class InputReplyToMessage(Object):
    """Contains information about a target replied message.

    Parameters:
        reply_to_message_id (``int``, *optional*):
            ID of the original message you want to reply.

        message_thread_id (``int``, *optional*):
            Unique identifier for the target message thread (topic) of the forum.
            for forum supergroups only.
    """

    def __init__(
        self, *,
        reply_to_message_id: int = None,
        message_thread_id: int = None
    ):
        super().__init__()

        self.reply_to_message_id = reply_to_message_id
        self.message_thread_id = message_thread_id

    def write(self):
        if not any((self.reply_to_message_id, self.message_thread_id)):
            return None

        return raw.types.InputReplyToMessage(
            reply_to_msg_id=self.reply_to_message_id or message_thread_id,  # type: ignore[arg-type]
            top_msg_id=self.message_thread_id if self.reply_to_message_id else None,
        ).write()

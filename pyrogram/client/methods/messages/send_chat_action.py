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
from pyrogram.client.ext import BaseClient, ChatAction


class SendChatAction(BaseClient):
    def send_chat_action(self,
                         chat_id: int or str,
                         action: ChatAction or str,
                         progress: int = 0):
        """Use this method when you need to tell the other party that something is happening on your side.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                For a private channel/supergroup you can use its *t.me/joinchat/* link.

            action (:obj:`ChatAction <pyrogram.ChatAction>` | ``str``):
                Type of action to broadcast.
                Choose one from the :class:`ChatAction <pyrogram.ChatAction>` enumeration,
                depending on what the user is about to receive.
                You can also provide a string (e.g. "typing", "upload_photo", "record_audio", ...).

            progress (``int``, *optional*):
                Progress of the upload process.
                Currently useless because official clients don't seem to be handling this.

        Returns:
            On success, True is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
            ``ValueError``: If the provided string is not a valid ChatAction
        """

        # Resolve Enum type
        if isinstance(action, str):
            action = ChatAction.from_string(action).value
        elif isinstance(action, ChatAction):
            action = action.value

        if "Upload" in action.__name__:
            action = action(progress)
        else:
            action = action()

        return self.send(
            functions.messages.SetTyping(
                peer=self.resolve_peer(chat_id),
                action=action
            )
        )

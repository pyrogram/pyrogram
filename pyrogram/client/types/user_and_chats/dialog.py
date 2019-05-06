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

import pyrogram

from pyrogram.api import types
from ..pyrogram_type import PyrogramType
from ..user_and_chats import Chat


class Dialog(PyrogramType):
    """This object represents a dialog.

    Args:
        chat (:obj:`Chat <pyrogram.Chat>`):
            Conversation the dialog belongs to.

        top_message (:obj:`Message <pyrogram.Message>`):
            The last message sent in the dialog at this time.

        unread_messages_count (``int``):
            Amount of unread messages in this dialog.

        unread_mentions_count (``int``):
            Amount of unread messages containing a mention in this dialog.

        unread_mark (``bool``):
            True, if the dialog has the unread mark set.

        is_pinned (``bool``):
            True, if the dialog is pinned.
    """

    __slots__ = ["chat", "top_message", "unread_messages_count", "unread_mentions_count", "unread_mark", "is_pinned"]

    def __init__(
        self,
        *,
        client: "pyrogram.client.ext.BaseClient",
        chat: Chat,
        top_message: "pyrogram.Message",
        unread_messages_count: int,
        unread_mentions_count: int,
        unread_mark: bool,
        is_pinned: bool
    ):
        super().__init__(client)

        self.chat = chat
        self.top_message = top_message
        self.unread_messages_count = unread_messages_count
        self.unread_mentions_count = unread_mentions_count
        self.unread_mark = unread_mark
        self.is_pinned = is_pinned

    @staticmethod
    def _parse(client, dialog, messages, users, chats) -> "Dialog":
        chat_id = dialog.peer

        if isinstance(chat_id, types.PeerUser):
            chat_id = chat_id.user_id
        elif isinstance(chat_id, types.PeerChat):
            chat_id = -chat_id.chat_id
        else:
            chat_id = int("-100" + str(chat_id.channel_id))

        return Dialog(
            chat=Chat._parse_dialog(client, dialog.peer, users, chats),
            top_message=messages.get(chat_id),
            unread_messages_count=dialog.unread_count,
            unread_mentions_count=dialog.unread_mentions_count,
            unread_mark=dialog.unread_mark,
            is_pinned=dialog.pinned,
            client=client
        )

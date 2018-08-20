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

from pyrogram.api.core import Object


class Dialog(Object):
    """This object represents a dialog

    Args:
        chat (:obj:`Chat <pyrogram.Chat>`):
            Conversation the dialog belongs to.

        top_message (:obj:`Message <pyrogram.Message>`):
            The last message sent in the dialog at this time.

        unread_messages_count (``int``):
            Amount of unread messages in this dialogs.

        unread_mentions_count (``int``):
            Amount of unread messages containing a mention in this dialog.

        unread_mark (``bool``):
            True, if the dialog has the unread mark set.

        is_pinned (``bool``):
            True, if the dialog is pinned.
    """
    ID = 0xb0700028

    def __init__(self,
                 chat,
                 top_message,
                 unread_messages_count: int,
                 unread_mentions_count: int,
                 unread_mark: bool,
                 is_pinned: bool):
        self.chat = chat
        self.top_message = top_message
        self.unread_messages_count = unread_messages_count
        self.unread_mentions_count = unread_mentions_count
        self.unread_mark = unread_mark
        self.is_pinned = is_pinned

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

from typing import List

import pyrogram
from pyrogram.api import types
from .dialog import Dialog
from ..messages_and_media import Message
from ..pyrogram_type import PyrogramType


class Dialogs(PyrogramType):
    """This object represents a user's dialogs chunk

    Args:
        total_count (``int``):
            Total number of dialogs the user has.

        dialogs (List of :obj:`Dialog <pyrogram.Dialog>`):
            Requested dialogs.
    """

    __slots__ = ["total_count", "dialogs"]

    def __init__(
            self,
            *,
            client: "pyrogram.client.ext.BaseClient",
            total_count: int,
            dialogs: List[Dialog]
    ):
        super().__init__(client)

        self.total_count = total_count
        self.dialogs = dialogs

    @staticmethod
    def _parse(client, dialogs) -> "Dialogs":
        users = {i.id: i for i in dialogs.users}
        chats = {i.id: i for i in dialogs.chats}

        messages = {}

        for message in dialogs.messages:
            to_id = message.to_id

            if isinstance(to_id, types.PeerUser):
                if message.out:
                    chat_id = to_id.user_id
                else:
                    chat_id = message.from_id
            elif isinstance(to_id, types.PeerChat):
                chat_id = -to_id.chat_id
            else:
                chat_id = int("-100" + str(to_id.channel_id))

            messages[chat_id] = Message._parse(client, message, users, chats)

        return Dialogs(
            total_count=getattr(dialogs, "count", len(dialogs.dialogs)),
            dialogs=[Dialog._parse(client, dialog, messages, users, chats) for dialog in dialogs.dialogs],
            client=client
        )

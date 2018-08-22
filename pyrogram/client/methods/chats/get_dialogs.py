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

import pyrogram
from pyrogram.api import functions, types
from ...ext import BaseClient, utils


class GetDialogs(BaseClient):
    async def get_dialogs(self,
                          offset_dialogs=None,
                          limit: int = 100,
                          pinned_only: bool = False):
        """Use this method to get the user's dialogs

        You can get up to 100 dialogs at once.

        Args:
            limit (``str``, *optional*):
                Limits the number of dialogs to be retrieved.
                Defaults to 100

            pinned_only (``bool``, *optional*):
                Pass True if you want to get only pinned dialogs.
                Defaults to False.

            offset_dialogs (:obj:`Dialogs`):
                Pass the previous dialogs object to retrieve the next dialogs chunk starting from the last dialog.
                Defaults to None (start from the beginning).

        Returns:
            On success, a :obj:`Dialogs` object is returned.

        Raises:
            :class:`Error`
        """

        if pinned_only:
            r = await self.send(functions.messages.GetPinnedDialogs())
        else:
            offset_date = 0

            if offset_dialogs:
                for dialog in reversed(offset_dialogs.dialogs):
                    top_message = dialog.top_message

                    if top_message:
                        message_date = top_message.date

                        if message_date:
                            offset_date = message_date
                            break

            r = await self.send(
                functions.messages.GetDialogs(
                    offset_date=offset_date,
                    offset_id=0,
                    offset_peer=types.InputPeerEmpty(),
                    limit=limit,
                    hash=0,
                    exclude_pinned=True
                )
            )

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}
        messages = {}

        for message in r.messages:
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

            messages[chat_id] = await utils.parse_messages(self, message, users, chats)

        dialogs = []

        for dialog in r.dialogs:
            chat_id = dialog.peer

            if isinstance(chat_id, types.PeerUser):
                chat_id = chat_id.user_id
            elif isinstance(chat_id, types.PeerChat):
                chat_id = -chat_id.chat_id
            else:
                chat_id = int("-100" + str(chat_id.channel_id))

            dialogs.append(
                pyrogram.Dialog(
                    chat=utils.parse_dialog_chat(dialog.peer, users, chats),
                    top_message=messages.get(chat_id),
                    unread_messages_count=dialog.unread_count,
                    unread_mentions_count=dialog.unread_mentions_count,
                    unread_mark=dialog.unread_mark,
                    is_pinned=dialog.pinned
                )
            )

        return pyrogram.Dialogs(
            total_count=getattr(r, "count", len(r.dialogs)),
            dialogs=dialogs
        )

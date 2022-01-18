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

from typing import Union, List

from pyrogram import raw
from pyrogram.scaffold import Scaffold


class ArchiveChats(Scaffold):
    async def archive_chats(
        self,
        chat_ids: Union[int, str, List[Union[int, str]]],
    ) -> bool:
        """Archive one or more chats.

        Parameters:
            chat_ids (``int`` | ``str`` | List[``int``, ``str``]):
                Unique identifier (int) or username (str) of the target chat.
                You can also pass a list of ids (int) or usernames (str).

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                # Archive chat
                app.archive_chats(chat_id)

                # Archive multiple chats at once
                app.archive_chats([chat_id1, chat_id2, chat_id3])
        """

        if not isinstance(chat_ids, list):
            chat_ids = [chat_ids]

        folder_peers = []

        for chat in chat_ids:
            folder_peers.append(
                raw.types.InputFolderPeer(
                    peer=await self.resolve_peer(chat),
                    folder_id=1
                )
            )

        await self.send(
            raw.functions.folders.EditPeerFolders(
                folder_peers=folder_peers
            )
        )

        return True

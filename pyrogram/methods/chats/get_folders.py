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

from typing import AsyncGenerator, Optional

import pyrogram
from pyrogram import types, raw


class GetFolders:
    async def get_folders(
        self: "pyrogram.Client",
    ) -> Optional[AsyncGenerator["types.Folder", None]]:
        """Get a user's folders with chats sequentially.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Folder` objects.

        Example:
            .. code-block:: python

                # Iterate through all folders
                async for folder in app.get_folders():
                    print(folder.title)
        """
        raw_folders = await self.invoke(raw.functions.messages.GetDialogFilters())
        dialog_peers = []

        for folder in raw_folders:
            if not isinstance(folder, (raw.types.DialogFilter, raw.types.DialogFilterChatlist)):
                continue

            peers = folder.pinned_peers + folder.include_peers + getattr(folder, "exclude_peers", [])
            input_peers = [raw.types.InputDialogPeer(peer=peer) for peer in peers] + [raw.types.InputDialogPeerFolder(folder_id=folder.id)]
            dialog_peers.extend(input_peers)

        r = await self.invoke(raw.functions.messages.GetPeerDialogs(peers=dialog_peers))

        users = {i.id: i for i in r.users}
        chats = {i.id: i for i in r.chats}
        peers = {**users, **chats}

        folders = []

        for folder in raw_folders:
            if not isinstance(folder, (raw.types.DialogFilter, raw.types.DialogFilterChatlist)):
                continue

            folders.append(types.Folder._parse(self, folder, peers))

        if not folders:
            return

        for folder in folders:
            yield folder

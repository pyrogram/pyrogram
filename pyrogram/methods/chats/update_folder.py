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

from typing import List, Union

import pyrogram
from pyrogram import raw


class UpdateFolder:
    async def update_folder(
        self: "pyrogram.Client",
        folder_id: int,
        title: str,
        pinned_peers: Union[Union[int, str], List[Union[int, str]]],
        included_peers: Union[Union[int, str], List[Union[int, str]]],
        excluded_peers: Union[Union[int, str], List[Union[int, str]]],
        contacts: bool = None,
        non_contacts: bool = None,
        groups: bool = None,
        broadcasts: bool = None,
        bots: bool = None,
        exclude_muted: bool = None,
        exclude_read: bool = None,
        exclude_archived: bool = None,
        emoji: str = None
    ) -> bool:
        """Create or update a user's folder.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``bool``: True, on success.

        Example:
            .. code-block:: python

                # Delete folder
                app.delete_folder(folder_id)
        """
        if not isinstance(pinned_peers, list):
            pinned_peers = [pinned_peers]
        if not isinstance(included_peers, list):
            included_peers = [included_peers]
        if not isinstance(excluded_peers, list):
            excluded_peers = [excluded_peers]

        r = await self.invoke(
            raw.functions.messages.UpdateDialogFilter(
                id=folder_id,
                filter=raw.types.DialogFilter(
                    id=folder_id,
                    title=title,
                    pinned_peers=[
                        await self.resolve_peer(user_id)
                        for user_id in pinned_peers
                    ],
                    include_peers=[
                        await self.resolve_peer(user_id)
                        for user_id in included_peers
                    ],
                    exclude_peers=[
                        await self.resolve_peer(user_id)
                        for user_id in excluded_peers
                    ],
                    contacts=contacts,
                    non_contacts=non_contacts,
                    groups=groups,
                    broadcasts=broadcasts,
                    bots=bots,
                    exclude_muted=exclude_muted,
                    exclude_read=exclude_read,
                    exclude_archived=exclude_archived,
                    emoticon=emoji
                )
            )
        )

        return r

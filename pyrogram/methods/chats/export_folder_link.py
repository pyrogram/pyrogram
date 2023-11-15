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

import pyrogram
from pyrogram import raw


class ExportFolderLink:
    async def export_folder_link(
        self: "pyrogram.Client",
        folder_id: int
    ) -> str:
        """Export link to a user's folder.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            ``str``: On success, a link to the folder as string is returned.

        Example:
            .. code-block:: python

                # Export folder link
                app.export_folder_link(123456789)
        """
        folder = await self.get_folder(folder_id)

        if not folder:
            return

        r = await self.invoke(
            raw.functions.chatlists.ExportChatlistInvite(
                chatlist=raw.types.InputChatlistDialogFilter(
                    filter_id=folder_id
                ),
                title=folder.title,
                peers=[await self.resolve_peer(i.id) for i in folder.pinned_peers] if folder.pinned_peers else []
                + [await self.resolve_peer(i.id) for i in folder.included_peers] if folder.included_peers else []
                + [await self.resolve_peer(i.id) for i in folder.excluded_peers] if folder.excluded_peers else [],
            )
        )

        return r.invite.url

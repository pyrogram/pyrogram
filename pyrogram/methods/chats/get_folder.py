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

from typing import Optional

import pyrogram
from pyrogram import types


class GetFolder:
    async def get_folder(
        self: "pyrogram.Client",
        folder_id: int
    ) -> Optional["types.Folder"]:
        """Get a user's folder by id.

        .. include:: /_includes/usable-by/users.rst

        Returns:
            :obj:`~pyrogram.types.Folder`: On success, the user's folder is returned.

        Example:
            .. code-block:: python

                # Get folder by id
                await app.get_folder(123456789)
        """
        async for folder in self.get_folders():
            if folder.id == folder_id:
                return folder

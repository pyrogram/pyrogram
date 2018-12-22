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
from ...ext import BaseClient


class GetDialogs(BaseClient):
    async def get_dialogs(self,
                          offset_dialog: "pyrogram.Dialog" = None,
                          limit: int = 100,
                          pinned_only: bool = False) -> "pyrogram.Dialogs":
        """Use this method to get the user's dialogs

        You can get up to 100 dialogs at once.

        Args:
            offset_dialog (:obj:`Dialog`):
                Sequential Dialog of the first dialog to be returned.
                Defaults to None (start from the beginning).

            limit (``str``, *optional*):
                Limits the number of dialogs to be retrieved.
                Defaults to 100.

            pinned_only (``bool``, *optional*):
                Pass True if you want to get only pinned dialogs.
                Defaults to False.

        Returns:
            On success, a :obj:`Dialogs` object is returned.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """

        if pinned_only:
            r = await self.send(functions.messages.GetPinnedDialogs())
        else:
            r = await self.send(
                functions.messages.GetDialogs(
                    offset_date=offset_dialog.top_message.date if offset_dialog else 0,
                    offset_id=0,
                    offset_peer=types.InputPeerEmpty(),
                    limit=limit,
                    hash=0,
                    exclude_pinned=True
                )
            )

        return pyrogram.Dialogs._parse(self, r)

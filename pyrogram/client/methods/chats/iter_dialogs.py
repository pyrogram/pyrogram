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

from typing import AsyncGenerator, Optional

from async_generator import async_generator, yield_

import pyrogram
from ...ext import BaseClient


class IterDialogs(BaseClient):
    @async_generator
    async def iter_dialogs(
        self,
        limit: int = 0,
        offset_date: int = 0
    ) -> Optional[AsyncGenerator["pyrogram.Dialog", None]]:
        """Use this method to iterate through a user's dialogs sequentially.

        This convenience method does the same as repeatedly calling :meth:`get_dialogs` in a loop, thus saving you from
        the hassle of setting up boilerplate code. It is useful for getting the whole dialogs list with a single call.

        Args:
            limit (``str``, *optional*):
                Limits the number of dialogs to be retrieved.
                By default, no limit is applied and all dialogs are returned.

            offset_date (``int``):
                The offset date in Unix time taken from the top message of a :obj:`Dialog`.
                Defaults to 0 (most recent dialog).

        Returns:
            A generator yielding :obj:`Dialog <pyrogram.Dialog>` objects.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        pinned_dialogs = (await self.get_dialogs(
            pinned_only=True
        )).dialogs

        for dialog in pinned_dialogs:
            await yield_(dialog)

            current += 1

            if current >= total:
                return

        while True:
            dialogs = (await self.get_dialogs(
                offset_date=offset_date,
                limit=limit
            )).dialogs

            if not dialogs:
                return

            offset_date = dialogs[-1].top_message.date

            for dialog in dialogs:
                await yield_(dialog)

                current += 1

                if current >= total:
                    return

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

import logging
from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types

log = logging.getLogger(__name__)


class GetStickers:
    async def get_stickers(
        self: "pyrogram.Client",
        short_name: str
    ) -> List["types.Sticker"]:
        """Get all stickers from set by short name.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            short_name (``str``):
                Short name of the sticker set, serves as the unique identifier for the sticker set.

        Returns:
            List of :obj:`~pyrogram.types.Sticker`: A list of stickers is returned.

        Example:
            .. code-block:: python

                # Get all stickers by short name
                await app.get_stickers("short_name")

        Raises:
            ValueError: In case of invalid arguments.
        """
        sticker_set = await self.invoke(
            raw.functions.messages.GetStickerSet(
                stickerset=raw.types.InputStickerSetShortName(short_name=short_name),
                hash=0
            )
        )

        return [
            await types.Sticker._parse(self, doc, {type(a): a for a in doc.attributes})
            for doc in sticker_set.documents
        ]

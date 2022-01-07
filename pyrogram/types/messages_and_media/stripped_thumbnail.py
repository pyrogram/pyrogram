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
from ..object import Object


class StrippedThumbnail(Object):
    """A stripped thumbnail

    Parameters:
        data (``bytes``):
            Thumbnail data
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        data: bytes
    ):
        super().__init__(client)

        self.data = data

    @staticmethod
    def _parse(client, stripped_thumbnail: "raw.types.PhotoStrippedSize") -> "StrippedThumbnail":
        return StrippedThumbnail(
            data=stripped_thumbnail.bytes,
            client=client
        )

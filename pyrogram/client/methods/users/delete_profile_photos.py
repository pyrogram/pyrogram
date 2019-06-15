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

from base64 import b64decode
from struct import unpack
from typing import List, Union

from pyrogram.api import functions, types
from ...ext import BaseClient


class DeleteProfilePhotos(BaseClient):
    def delete_profile_photos(
        self,
        id: Union[str, List[str]]
    ) -> bool:
        """Delete your own profile photos.

        Parameters:
            id (``str`` | ``list``):
                A single :obj:`Photo` id as string or multiple ids as list of strings for deleting
                more than one photos at once.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        id = id if isinstance(id, list) else [id]
        input_photos = []

        for i in id:
            s = unpack("<qq", b64decode(i + "=" * (-len(i) % 4), "-_"))

            input_photos.append(
                types.InputPhoto(
                    id=s[0],
                    access_hash=s[1],
                    file_reference=b""
                )
            )

        return bool(self.send(
            functions.photos.DeletePhotos(
                id=input_photos
            )
        ))

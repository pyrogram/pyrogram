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

from struct import unpack
from typing import List, Union

from pyrogram.api import functions, types
from pyrogram.client.ext import utils
from ...ext import BaseClient


class DeleteProfilePhotos(BaseClient):
    async def delete_profile_photos(
        self,
        photo_ids: Union[str, List[str]]
    ) -> bool:
        """Delete your own profile photos.

        Parameters:
            photo_ids (``str`` | List of ``str``):
                A single :obj:`Photo` id as string or multiple ids as list of strings for deleting
                more than one photos at once.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Get the photos to be deleted
                photos = app.get_profile_photos("me")

                # Delete one photo
                app.delete_profile_photos(photos[0].file_id)

                # Delete the rest of the photos
                app.delete_profile_photos([p.file_id for p in photos[1:]])
        """
        photo_ids = photo_ids if isinstance(photo_ids, list) else [photo_ids]
        input_photos = []

        for photo_id in photo_ids:
            unpacked = unpack("<iiqqc", utils.decode_file_id(photo_id))

            input_photos.append(
                types.InputPhoto(
                    id=unpacked[2],
                    access_hash=unpacked[3],
                    file_reference=b""
                )
            )

        return bool(await self.send(
            functions.photos.DeletePhotos(
                id=input_photos
            )
        ))

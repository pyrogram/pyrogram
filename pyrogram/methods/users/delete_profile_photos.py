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
from pyrogram import utils
from pyrogram.file_id import FileType


class DeleteProfilePhotos:
    async def delete_profile_photos(
        self: "pyrogram.Client",
        photo_ids: Union[str, List[str]]
    ) -> bool:
        """Delete your own profile photos.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            photo_ids (``str`` | List of ``str``):
                A single :obj:`~pyrogram.types.Photo` id as string or multiple ids as list of strings for deleting
                more than one photos at once.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Get the photos to be deleted
                photos = [p async for p in app.get_chat_photos("me")]

                # Delete one photo
                await app.delete_profile_photos(photos[0].file_id)

                # Delete the rest of the photos
                await app.delete_profile_photos([p.file_id for p in photos[1:]])
        """
        photo_ids = photo_ids if isinstance(photo_ids, list) else [photo_ids]
        input_photos = [utils.get_input_media_from_file_id(i, FileType.PHOTO).id for i in photo_ids]

        return bool(await self.invoke(
            raw.functions.photos.DeletePhotos(
                id=input_photos
            )
        ))

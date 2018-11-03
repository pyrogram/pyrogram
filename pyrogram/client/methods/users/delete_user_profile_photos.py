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

from base64 import b64decode
from struct import unpack

from pyrogram.api import functions, types
from ...ext import BaseClient


class DeleteUserProfilePhotos(BaseClient):
    def delete_user_profile_photos(self, id: str or list):
        """Use this method to delete your own profile photos

        Args:
            id (``str`` | ``list``):
                A single :obj:`Photo <pyrogram.Photo>` id as string or multiple ids as list of strings for deleting
                more than one photos at once.

        Returns:
            True on success.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """
        id = id if isinstance(id, list) else [id]
        input_photos = []

        for i in id:
            s = unpack("<qq", b64decode(i + "=" * (-len(i) % 4), "-_"))

            input_photos.append(
                types.InputPhoto(
                    id=s[0],
                    access_hash=s[1]
                )
            )

        return bool(self.send(
            functions.photos.DeletePhotos(
                id=input_photos
            )
        ))

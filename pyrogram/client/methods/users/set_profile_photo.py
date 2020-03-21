#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

from pyrogram.api import functions
from ...ext import BaseClient


class SetProfilePhoto(BaseClient):
    def set_profile_photo(
        self,
        photo: str
    ) -> bool:
        """Set a new profile photo.

        This method only works for Users.
        Bots profile photos must be set using BotFather.

        Parameters:
            photo (``str``):
                Profile photo to set.
                Pass a file path as string to upload a new photo that exists on your local machine.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                app.set_profile_photo("new_photo.jpg")
        """

        return bool(
            self.send(
                functions.photos.UploadProfilePhoto(
                    file=self.save_file(photo)
                )
            )
        )

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

from typing import Union, BinaryIO

from pyrogram.api import functions
from ...ext import BaseClient


class SetProfileVideo(BaseClient):
    def set_profile_video(
        self,
        video: Union[str, BinaryIO]
    ) -> bool:
        """Set a new profile video (H.264/MPEG-4 AVC video, max 5 seconds).

        If you want to set a profile photo instead, use :meth:`~Client.set_profile_photo`

        This method only works for Users.

        Parameters:
            video (``str``):
                Profile video to set.
                Pass a file path as string to upload a new video that exists on your local machine or
                pass a binary file-like object with its attribute ".name" set for in-memory uploads.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                app.set_profile_video("new_video.mp4")
        """

        return bool(
            self.send(
                functions.photos.UploadProfilePhoto(
                    video=self.save_file(video)
                )
            )
        )

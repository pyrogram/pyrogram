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

from typing import List

import pyrogram
from .photo import Photo
from ..pyrogram_type import PyrogramType


class UserProfilePhotos(PyrogramType):
    """This object represents a user's profile pictures.

    Parameters:
        total_count (``int``):
            Total number of profile pictures the target user has.

        photos (List of :obj:`Photo`):
            Requested profile pictures.
    """

    __slots__ = ["total_count", "photos"]

    def __init__(
        self,
        *,
        client: "pyrogram.client.ext.BaseClient",
        total_count: int,
        photos: List[Photo]
    ):
        super().__init__(client)

        self.total_count = total_count
        self.photos = photos

    @staticmethod
    def _parse(client, photos) -> "UserProfilePhotos":
        return UserProfilePhotos(
            total_count=getattr(photos, "count", len(photos.photos)),
            photos=[Photo._parse(client, photo) for photo in photos.photos],
            client=client
        )

#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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

from typing import Union

import pyrogram
from pyrogram import raw
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType, ThumbnailSource
from ..object import Object


class ChatPhoto(Object):
    """A chat photo.

    Parameters:
        small_file_id (``str``):
            File identifier of small (160x160) chat photo.
            This file_id can be used only for photo download and only for as long as the photo is not changed.

        small_photo_unique_id (``str``):
            Unique file identifier of small (160x160) chat photo, which is supposed to be the same over time and for
            different accounts. Can't be used to download or reuse the file.

        big_file_id (``str``):
            File identifier of big (640x640) chat photo.
            This file_id can be used only for photo download and only for as long as the photo is not changed.

        big_photo_unique_id (``str``):
            Unique file identifier of big (640x640) chat photo, which is supposed to be the same over time and for
            different accounts. Can't be used to download or reuse the file.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        small_file_id: str,
        small_photo_unique_id: str,
        big_file_id: str,
        big_photo_unique_id: str

    ):
        super().__init__(client)

        self.small_file_id = small_file_id
        self.small_photo_unique_id = small_photo_unique_id
        self.big_file_id = big_file_id
        self.big_photo_unique_id = big_photo_unique_id

    @staticmethod
    def _parse(
        client,
        chat_photo: Union["raw.types.UserProfilePhoto", "raw.types.ChatPhoto"],
        peer_id: int,
        peer_access_hash: int
    ):
        if not isinstance(chat_photo, (raw.types.UserProfilePhoto, raw.types.ChatPhoto)):
            return None

        media_id = chat_photo.photo_id if isinstance(chat_photo, raw.types.UserProfilePhoto) else 0

        return ChatPhoto(
            small_file_id=FileId(
                file_type=FileType.CHAT_PHOTO,
                dc_id=chat_photo.dc_id,
                media_id=media_id,
                access_hash=0,
                volume_id=chat_photo.photo_small.volume_id,
                thumbnail_source=ThumbnailSource.CHAT_PHOTO_SMALL,
                local_id=chat_photo.photo_small.local_id,
                chat_id=peer_id,
                chat_access_hash=peer_access_hash
            ).encode(),
            small_photo_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.PHOTO,
                volume_id=chat_photo.photo_small.volume_id,
                local_id=chat_photo.photo_small.local_id
            ).encode(),
            big_file_id=FileId(
                file_type=FileType.CHAT_PHOTO,
                dc_id=chat_photo.dc_id,
                media_id=media_id,
                access_hash=0,
                volume_id=chat_photo.photo_big.volume_id,
                thumbnail_source=ThumbnailSource.CHAT_PHOTO_BIG,
                local_id=chat_photo.photo_big.local_id,
                chat_id=peer_id,
                chat_access_hash=peer_access_hash
            ).encode(),
            big_photo_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.PHOTO,
                volume_id=chat_photo.photo_big.volume_id,
                local_id=chat_photo.photo_big.local_id
            ).encode(),
            client=client
        )

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

from typing import List

from async_lru import alru_cache

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.errors import StickersetInvalid
from pyrogram.file_id import FileId, FileType, FileUniqueId, FileUniqueType
from ..object import Object


class Sticker(Object):
    """A sticker.

    Parameters:
        file_id (``str``):
            Identifier for this file, which can be used to download or reuse the file.

        file_unique_id (``str``):
            Unique identifier for this file, which is supposed to be the same over time and for different accounts.
            Can't be used to download or reuse the file.

        width (``int``):
            Sticker width.

        height (``int``):
            Sticker height.

        is_animated (``bool``):
            True, if the sticker is animated

        file_name (``str``, *optional*):
            Sticker file name.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the sticker was sent in Unix time.

        emoji (``str``, *optional*):
            Emoji associated with the sticker.

        set_name (``str``, *optional*):
            Name of the sticker set to which the sticker belongs.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Sticker thumbnails in the .webp or .jpg format.
    """

    # TODO: Add mask position

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_unique_id: str,
        width: int,
        height: int,
        is_animated: bool,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: int = None,
        emoji: str = None,
        set_name: str = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_unique_id = file_unique_id
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.width = width
        self.height = height
        self.is_animated = is_animated
        self.emoji = emoji
        self.set_name = set_name
        self.thumbs = thumbs
        # self.mask_position = mask_position

    @staticmethod
    @alru_cache(maxsize=256)
    async def _get_sticker_set_name(send, input_sticker_set_id):
        try:
            return (await send(
                raw.functions.messages.GetStickerSet(
                    stickerset=raw.types.InputStickerSetID(
                        id=input_sticker_set_id[0],
                        access_hash=input_sticker_set_id[1]
                    )
                )
            )).set.short_name
        except StickersetInvalid:
            return None

    @staticmethod
    async def _parse(
        client,
        sticker: "raw.types.Document",
        image_size_attributes: "raw.types.DocumentAttributeImageSize",
        sticker_attributes: "raw.types.DocumentAttributeSticker",
        file_name: str
    ) -> "Sticker":
        sticker_set = sticker_attributes.stickerset

        if isinstance(sticker_set, raw.types.InputStickerSetID):
            input_sticker_set_id = (sticker_set.id, sticker_set.access_hash)
            set_name = await Sticker._get_sticker_set_name(client.send, input_sticker_set_id)
        else:
            set_name = None

        return Sticker(
            file_id=FileId(
                file_type=FileType.STICKER,
                dc_id=sticker.dc_id,
                media_id=sticker.id,
                access_hash=sticker.access_hash,
                file_reference=sticker.file_reference
            ).encode(),
            file_unique_id=FileUniqueId(
                file_unique_type=FileUniqueType.DOCUMENT,
                media_id=sticker.id
            ).encode(),
            width=image_size_attributes.w if image_size_attributes else 512,
            height=image_size_attributes.h if image_size_attributes else 512,
            is_animated=sticker.mime_type == "application/x-tgsticker",
            # TODO: mask_position
            set_name=set_name,
            emoji=sticker_attributes.alt or None,
            file_size=sticker.size,
            mime_type=sticker.mime_type,
            file_name=file_name,
            date=sticker.date,
            thumbs=types.Thumbnail._parse(client, sticker),
            client=client
        )

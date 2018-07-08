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

from pyrogram.api.core import Object


class Sticker(Object):
    """This object represents a sticker.

    Args:
        file_id (``str``):
            Unique identifier for this file.

        width (``int``):
            Sticker width.

        height (``int``):
            Sticker height.

        thumb (:obj:`PhotoSize <pyrogram.PhotoSize>`, *optional*):
            Sticker thumbnail in the .webp or .jpg format.

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

        mask_position (:obj:`MaskPosition <pyrogram.MaskPosition>`, *optional*):
            For mask stickers, the position where the mask should be placed.
    """

    ID = 0xb0700017

    def __init__(
            self,
            file_id: str,
            width: int,
            height: int,
            thumb=None,
            file_name: str = None,
            mime_type: str = None,
            file_size: int = None,
            date: int = None,
            emoji: str = None,
            set_name: str = None,
            mask_position=None
    ):
        self.file_id = file_id  # string
        self.thumb = thumb  # flags.0?PhotoSize
        self.file_name = file_name  # flags.1?string
        self.mime_type = mime_type  # flags.2?string
        self.file_size = file_size  # flags.3?int
        self.date = date  # flags.4?int
        self.width = width  # int
        self.height = height  # int
        self.emoji = emoji  # flags.5?string
        self.set_name = set_name  # flags.6?string
        self.mask_position = mask_position  # flags.7?MaskPosition

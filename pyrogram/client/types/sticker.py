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

    Attributes:
        ID: ``0xb0700017``

    Args:
        file_id (``str``):
            Unique identifier for this file.

        width (``int`` ``32-bit``):
            Sticker width.

        height (``int`` ``32-bit``):
            Sticker height.

        thumb (:obj:`PhotoSize <pyrogram.types.PhotoSize>`, optional):
            Sticker thumbnail in the .webp or .jpg format.

        emoji (``str``, optional):
            Emoji associated with the sticker.

        set_name (``str``, optional):
            Name of the sticker set to which the sticker belongs.

        mask_position (:obj:`MaskPosition <pyrogram.types.MaskPosition>`, optional):
            For mask stickers, the position where the mask should be placed.

        file_size (``int`` ``32-bit``, optional):
            File size.

    """
    ID = 0xb0700017

    def __init__(self, file_id, width, height, thumb=None, emoji=None, set_name=None, mask_position=None, file_size=None):
        self.file_id = file_id  # string
        self.width = width  # int
        self.height = height  # int
        self.thumb = thumb  # flags.0?PhotoSize
        self.emoji = emoji  # flags.1?string
        self.set_name = set_name  # flags.2?string
        self.mask_position = mask_position  # flags.3?MaskPosition
        self.file_size = file_size  # flags.4?int

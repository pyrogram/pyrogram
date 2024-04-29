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

from typing import Optional, Union

from pyrogram import raw
from pyrogram import enums
from ..object import Object


class ChatColor(Object):
    """Reply or profile color status.

    Parameters:
        color (:obj:`~pyrogram.enums.ReplyColor` | :obj:`~pyrogram.enums.ProfileColor`, *optional*):
            Color type.

        background_emoji_id (``int``, *optional*):
            Unique identifier of the custom emoji.
    """

    def __init__(
        self,
        *,
        color: Union["enums.ReplyColor", "enums.ProfileColor"] = None,
        background_emoji_id: int = None
    ):
        self.color = color
        self.background_emoji_id = background_emoji_id

    @staticmethod
    def _parse(color: "raw.types.PeerColor" = None) -> Optional["ChatColor"]:
        if not color:
            return None

        return ChatColor(
            color=enums.ReplyColor(color.color) if getattr(color, "color", None) else None,
            background_emoji_id=getattr(color, "background_emoji_id", None)
        )

    @staticmethod
    def _parse_profile_color(color: "raw.types.PeerColor" = None) -> Optional["ChatColor"]:
        if not color:
            return None

        return ChatColor(
            color=enums.ProfileColor(color.color) if getattr(color, "color", None) else None,
            background_emoji_id=getattr(color, "background_emoji_id", None)
        )

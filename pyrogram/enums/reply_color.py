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

from .auto_name import AutoName


class ReplyColor(AutoName):
    """Reply color enumeration used in :meth:`~pyrogram.Client.update_color` and :obj:`~pyrogram.types.ChatColor`."""

    RED = 0
    "Red color."

    ORANGE = 1
    "Orange color."

    VIOLET = 2
    "Violet color."

    GREEN = 3
    "Green color."

    CYAN = 4
    "Cyan color."

    BLUE = 5
    "Blue color."

    PINK = 6
    "Pink color."

    RED_DARK_RED = 7
    "Red color with dark red stripes."

    ORANGE_DARK_ORANGE = 8
    "Orange color with dark orange stripes."

    VIOLET_DARK_VIOLET = 9
    "Violet color with dark violet stripes."

    GREEN_DARK_GREEN = 10
    "Green color with dark green stripes."

    CYAN_DARK_CYAN = 11
    "Cyan color with dark cyan stripes."

    BLUE_DARK_BLUE = 12
    "Blue color with dark blue stripes."

    PINK_DARK_PINK = 13
    "Pink color with dark pink stripes."

    BLUE_WHITE_RED = 14
    "Blue color with white and red stripes."

    ORANGE_WHITE_GREEN = 15
    "Orange color with white and green stripes."

    GREEN_WHITE_RED = 16
    "Green color with white and red stripes."

    CYAN_WHITE_GREEN = 17
    "Cyan color with white and red green."

    CYAN_YELLOW_PINK = 18
    "Cyan color with yellow and pink stripes."

    VIOLET_YELLOW_ORANGE = 19
    "Violet color with yellow and orange stripes."

    BLUE_WHITE_ORANGE = 20
    "Blue color with white and orange stripes."

    DYNAMIC = 21
    """Secret color that cannot be set.

    For now:
    Red - If you use Telegram desktop.
    Blue - If you are using Telegram android/ios.
    """

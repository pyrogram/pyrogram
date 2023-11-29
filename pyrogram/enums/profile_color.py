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


class ProfileColor(AutoName):
    """Profile color enumeration used in :obj:`~pyrogram.method.UpdateColor`."""

    RED = 0
    ORANGE = 1
    VIOLET = 2
    GREEN = 3
    CYAN = 4
    BLUE = 5
    PINK = 6

    RED_DARK_RED = 7
    ORANGE_DARK_ORANGE = 8
    VIOLET_DARK_VIOLET = 9
    GREEN_DARK_GREEN = 10
    CYAN_DARK_CYAN = 11
    BLUE_DARK_BLUE = 12
    PINK_DARK_PINK = 13

    BLUE_WHITE_RED = 14
    ORANGE_WHITE_GREEN = 15
    GREEN_WHITE_RED = 16
    BLUE_WHITE_GREEN = 17
    BLUE_WHITE_PINK = 18
    VIOLET_WHITE_ORANGE = 19
    BLUE_WHITE_ORANGE = 20

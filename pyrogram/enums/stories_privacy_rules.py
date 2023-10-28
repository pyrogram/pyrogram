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

from enum import auto
from .auto_name import AutoName


class StoriesPrivacyRules(AutoName):
    """Stories privacy rules type enumeration used in :obj:`~pyrogram.method.SendStory`."""

    PUBLIC = auto()
    "Public stories"

    CONTACTS = auto()
    "Contacts only stories"

    CLOSE_FRIENDS = auto()
    "Close friends stories"

    SELECTED_USERS = auto()
    "Selected users stories"

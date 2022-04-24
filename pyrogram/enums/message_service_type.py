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


class MessageServiceType(AutoName):
    """Message service type enumeration used in :obj:`~pyrogram.types.Message`."""

    NEW_CHAT_MEMBERS = auto()
    "New members join"

    LEFT_CHAT_MEMBERS = auto()
    "Left chat members"

    NEW_CHAT_TITLE = auto()
    "New chat title"

    NEW_CHAT_PHOTO = auto()
    "New chat photo"

    DELETE_CHAT_PHOTO = auto()
    "Deleted chat photo"

    GROUP_CHAT_CREATED = auto()
    "Group chat created"

    CHANNEL_CHAT_CREATED = auto()
    "Channel chat created"

    MIGRATE_TO_CHAT_ID = auto()
    "Migrated to chat id"

    MIGRATE_FROM_CHAT_ID = auto()
    "Migrated from chat id"

    PINNED_MESSAGE = auto()
    "Pinned message"

    GAME_HIGH_SCORE = auto()
    "Game high score"

    VIDEO_CHAT_STARTED = auto()
    "Video chat started"

    VIDEO_CHAT_ENDED = auto()
    "Video chat ended"

    VIDEO_CHAT_SCHEDULED = auto()
    "Video chat scheduled"

    VIDEO_CHAT_MEMBERS_INVITED = auto()
    "Video chat members invited"

    WEB_APP_DATA = auto()
    "Web app data"

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

from pyrogram import raw
from .auto_name import AutoName


class MessagesFilter(AutoName):
    """Messages filter enumeration used in :meth:`~pyrogram.Client.search_messages` and :meth:`~pyrogram.Client.search_global`"""

    EMPTY = raw.types.InputMessagesFilterEmpty
    "Empty filter (any kind of messages)"

    PHOTO = raw.types.InputMessagesFilterPhotos
    "Photo messages"

    VIDEO = raw.types.InputMessagesFilterVideo
    "Video messages"

    PHOTO_VIDEO = raw.types.InputMessagesFilterPhotoVideo
    "Photo and video messages"

    DOCUMENT = raw.types.InputMessagesFilterDocument
    "Document messages"

    URL = raw.types.InputMessagesFilterUrl
    "Messages containing URLs"

    ANIMATION = raw.types.InputMessagesFilterGif
    "Animation messages"

    VOICE_NOTE = raw.types.InputMessagesFilterVoice
    "Voice note messages"

    VIDEO_NOTE = raw.types.InputMessagesFilterRoundVideo
    "Video note messages"

    AUDIO_VIDEO_NOTE = raw.types.InputMessagesFilterRoundVideo
    "Audio and video note messages"

    AUDIO = raw.types.InputMessagesFilterMusic
    "Audio messages (music)"

    CHAT_PHOTO = raw.types.InputMessagesFilterChatPhotos
    "Chat photo messages"

    PHONE_CALL = raw.types.InputMessagesFilterPhoneCalls
    "Phone call messages"

    MENTION = raw.types.InputMessagesFilterMyMentions
    "Messages containing mentions"

    LOCATION = raw.types.InputMessagesFilterGeo
    "Location messages"

    CONTACT = raw.types.InputMessagesFilterContacts
    "Contact messages"

    PINNED = raw.types.InputMessagesFilterPinned
    "Pinned messages"

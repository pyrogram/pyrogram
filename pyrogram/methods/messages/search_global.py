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

from typing import AsyncGenerator, Optional

from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from pyrogram.scaffold import Scaffold


class Filters:
    EMPTY = raw.types.InputMessagesFilterEmpty()
    PHOTO = raw.types.InputMessagesFilterPhotos()
    VIDEO = raw.types.InputMessagesFilterVideo()
    PHOTO_VIDEO = raw.types.InputMessagesFilterPhotoVideo()
    DOCUMENT = raw.types.InputMessagesFilterDocument()
    URL = raw.types.InputMessagesFilterUrl()
    ANIMATION = raw.types.InputMessagesFilterGif()
    VOICE_NOTE = raw.types.InputMessagesFilterVoice()
    AUDIO = raw.types.InputMessagesFilterMusic()
    CHAT_PHOTO = raw.types.InputMessagesFilterChatPhotos()
    AUDIO_VIDEO_NOTE = raw.types.InputMessagesFilterRoundVideo()
    VIDEO_NOTE = raw.types.InputMessagesFilterRoundVideo()
    LOCATION = raw.types.InputMessagesFilterGeo()
    CONTACT = raw.types.InputMessagesFilterContacts()


POSSIBLE_VALUES = list(map(lambda x: x.lower(), filter(lambda x: not x.startswith("__"), Filters.__dict__.keys())))


class SearchGlobal(Scaffold):
    async def search_global(
        self,
        query: str = "",
        filter: str = "empty",
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Search messages globally from all of your chats.

        .. note::

            Due to server-side limitations, you can only get up to around ~10,000 messages and each message
            retrieved will not have any *reply_to_message* field.

        Parameters:
            query (``str``, *optional*):
                Text query string.
                Use "@" to search for mentions.
            
            filter (``str``, *optional*):
                Pass a filter in order to search for specific kind of messages only:

                - ``"empty"``: Search for all kind of messages (default).
                - ``"photo"``: Search for photos.
                - ``"video"``: Search for video.
                - ``"photo_video"``: Search for either photo or video.
                - ``"document"``: Search for documents (generic files).
                - ``"url"``: Search for messages containing URLs (web links).
                - ``"animation"``: Search for animations (GIFs).
                - ``"voice_note"``: Search for voice notes.
                - ``"audio"``: Search for audio files (music).
                - ``"chat_photo"``: Search for chat photos.
                - ``"audio_video_note"``: Search for either audio or video notes.
                - ``"video_note"``: Search for video notes.
                - ``"location"``: Search for location messages.
                - ``"contact"``: Search for contact messages.

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Message` objects.

        Example:
            .. code-block:: python

                # Search for "pyrogram". Get the first 420 results
                for message in app.search_global("pyrogram", limit=420):
                    print(message.text)

                # Search for recent photos from Global. Get the first 69 results
                for message in app.search_global(filter="photo", limit=69):
                    print(message.photo)
        """
        try:
            filter = Filters.__dict__[filter.upper()]
        except KeyError:
            raise ValueError('Invalid filter "{}". Possible values are: {}'.format(
                filter, ", ".join(f'"{v}"' for v in POSSIBLE_VALUES))) from None
        current = 0
        # There seems to be an hard limit of 10k, beyond which Telegram starts spitting one message at a time.
        total = abs(limit) or (1 << 31)
        limit = min(100, total)

        offset_date = 0
        offset_peer = raw.types.InputPeerEmpty()
        offset_id = 0

        while True:
            messages = await utils.parse_messages(
                self,
                await self.send(
                    raw.functions.messages.SearchGlobal(
                        q=query,
                        filter=filter,
                        min_date=0,
                        max_date=0,
                        offset_rate=offset_date,
                        offset_peer=offset_peer,
                        offset_id=offset_id,
                        limit=limit
                    ),
                    sleep_threshold=60
                ),
                replies=0
            )

            if not messages:
                return

            last = messages[-1]

            offset_date = last.date
            offset_peer = await self.resolve_peer(last.chat.id)
            offset_id = last.message_id

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return

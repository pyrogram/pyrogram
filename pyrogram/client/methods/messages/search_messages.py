#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

from typing import Union, List, Generator

import pyrogram
from pyrogram.client.ext import BaseClient, utils
from pyrogram.api import functions, types


class Filters:
    EMPTY = types.InputMessagesFilterEmpty()
    PHOTO = types.InputMessagesFilterPhotos()
    VIDEO = types.InputMessagesFilterVideo()
    PHOTO_VIDEO = types.InputMessagesFilterPhotoVideo()
    DOCUMENT = types.InputMessagesFilterDocument()
    URL = types.InputMessagesFilterUrl()
    ANIMATION = types.InputMessagesFilterGif()
    VOICE_NOTE = types.InputMessagesFilterVoice()
    AUDIO = types.InputMessagesFilterMusic()
    CHAT_PHOTO = types.InputMessagesFilterChatPhotos()
    PHONE_CALL = types.InputMessagesFilterPhoneCalls()
    AUDIO_VIDEO_NOTE = types.InputMessagesFilterRoundVideo()
    VIDEO_NOTE = types.InputMessagesFilterRoundVideo()
    MENTION = types.InputMessagesFilterMyMentions()
    LOCATION = types.InputMessagesFilterGeo()
    CONTACT = types.InputMessagesFilterContacts()


POSSIBLE_VALUES = list(map(lambda x: x.lower(), filter(lambda x: not x.startswith("__"), Filters.__dict__.keys())))


# noinspection PyShadowingBuiltins
def get_chunk(
    client: BaseClient,
    chat_id: Union[int, str],
    query: str = "",
    filter: str = "empty",
    offset: int = 0,
    limit: int = 100,
    from_user: Union[int, str] = None
) -> List["pyrogram.Message"]:
    try:
        filter = Filters.__dict__[filter.upper()]
    except KeyError:
        raise ValueError('Invalid filter "{}". Possible values are: {}'.format(
            filter, ", ".join('"{}"'.format(v) for v in POSSIBLE_VALUES))) from None

    r = client.send(
        functions.messages.Search(
            peer=client.resolve_peer(chat_id),
            q=query,
            filter=filter,
            min_date=0,
            max_date=0,
            offset_id=0,
            add_offset=offset,
            limit=limit,
            min_id=0,
            max_id=0,
            from_id=(
                client.resolve_peer(from_user)
                if from_user
                else None
            ),
            hash=0
        )
    )

    return utils.parse_messages(client, r)


class SearchMessages(BaseClient):
    # noinspection PyShadowingBuiltins
    def search_messages(
        self,
        chat_id: Union[int, str],
        query: str = "",
        offset: int = 0,
        filter: str = "empty",
        limit: int = 0,
        from_user: Union[int, str] = None
    ) -> Generator["pyrogram.Message", None, None]:
        """Search for text and media messages inside a specific chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            query (``str``, *optional*):
                Text query string.
                Required for text-only messages, optional for media messages (see the ``filter`` argument).
                When passed while searching for media messages, the query will be applied to captions.
                Defaults to "" (empty string).

            offset (``int``, *optional*):
                Sequential number of the first message to be returned.
                Defaults to 0.

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
                - ``"phone_call"``: Search for phone calls.
                - ``"audio_video_note"``: Search for either audio or video notes.
                - ``"video_note"``: Search for video notes.
                - ``"mention"``: Search for messages containing mentions to yourself.
                - ``"location"``: Search for location messages.
                - ``"contact"``: Search for contact messages.

            limit (``int``, *optional*):
                Limits the number of messages to be retrieved.
                By default, no limit is applied and all messages are returned.

            from_user (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user you want to search for messages from.

        Returns:
            ``Generator``: A generator yielding :obj:`Message` objects.

        Example:
            .. code-block:: python

                # Search for text messages in @pyrogramchat. Get the last 333 results
                for message in app.search_messages("pyrogramchat", query="dan", limit=333):
                    print(message.text)

                # Search for photos sent by @haskell in @pyrogramchat
                for message in app.search_messages("pyrogramchat", "", filter="photo" limit=333, from_user="haskell"):
                    print(message.text)
        """
        current = 0
        total = abs(limit) or (1 << 31) - 1
        limit = min(100, total)

        while True:
            messages = get_chunk(
                client=self,
                chat_id=chat_id,
                query=query,
                filter=filter,
                offset=offset,
                limit=limit,
                from_user=from_user
            )

            if not messages:
                return

            offset += 100

            for message in messages:
                yield message

                current += 1

                if current >= total:
                    return

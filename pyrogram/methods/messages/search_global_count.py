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
from pyrogram.scaffold import Scaffold
from .search_messages import Filters, POSSIBLE_VALUES


class SearchGlobalCount(Scaffold):
    async def search_global_count(
        self,
        query: str = "",
        filter: str = "empty",
    ) -> int:
        """Get the count of messages resulting from a global search.

        If you want to get the actual messages, see :meth:`~pyrogram.Client.search_global`.

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

        Returns:
            ``int``: On success, the messages count is returned.
        """
        try:
            filter = Filters.__dict__[filter.upper()]
        except KeyError:
            raise ValueError('Invalid filter "{}". Possible values are: {}'.format(
                filter, ", ".join(f'"{v}"' for v in POSSIBLE_VALUES))) from None

        r = await self.send(
            raw.functions.messages.SearchGlobal(
                q=query,
                filter=filter,
                min_date=0,
                max_date=0,
                offset_rate=0,
                offset_peer=raw.types.InputPeerEmpty(),
                offset_id=0,
                limit=1
            )
        )

        if hasattr(r, "count"):
            return r.count
        else:
            return len(r.messages)

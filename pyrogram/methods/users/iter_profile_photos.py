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

from typing import Union, AsyncGenerator, Optional

from pyrogram import types
from pyrogram.scaffold import Scaffold


class IterProfilePhotos(Scaffold):
    async def iter_profile_photos(
        self,
        chat_id: Union[int, str],
        offset: int = 0,
        limit: int = 0,
    ) -> Optional[AsyncGenerator["types.Message", None]]:
        """Iterate through a chat or a user profile photos sequentially.

        This convenience method does the same as repeatedly calling :meth:`~pyrogram.Client.get_profile_photos` in a
        loop, thus saving you from the hassle of setting up boilerplate code. It is useful for getting all the profile
        photos with a single call.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            limit (``int``, *optional*):
                Limits the number of profile photos to be retrieved.
                By default, no limit is applied and all profile photos are returned.

            offset (``int``, *optional*):
                Sequential number of the first profile photo to be returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.Photo` objects.

        Example:
            .. code-block:: python

                for photo in app.iter_profile_photos("haskell"):
                    print(photo.file_id)
        """
        current = 0
        total = limit or (1 << 31)
        limit = min(100, total)

        while True:
            photos = await self.get_profile_photos(
                chat_id=chat_id,
                offset=offset,
                limit=limit
            )

            if not photos:
                return

            offset += len(photos)

            for photo in photos:
                yield photo

                current += 1

                if current >= total:
                    return

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

from typing import Union, List

from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from pyrogram.scaffold import Scaffold


class GetProfilePhotos(Scaffold):
    async def get_profile_photos(
        self,
        chat_id: Union[int, str],
        offset: int = 0,
        limit: int = 100
    ) -> List["types.Photo"]:
        """Get a list of profile pictures for a user or a chat.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            offset (``int``, *optional*):
                Sequential number of the first photo to be returned.
                By default, all photos are returned.

            limit (``int``, *optional*):
                Limits the number of photos to be retrieved.
                Values between 1—100 are accepted. Defaults to 100.

        Returns:
            List of :obj:`~pyrogram.types.Photo`: On success, a list of profile photos is returned.

        Example:
            .. code-block:: python

                # Get the first 100 profile photos of a user
                app.get_profile_photos("me")

                # Get only the first profile photo of a user
                app.get_profile_photos("me", limit=1)

                # Get 3 profile photos of a user, skip the first 5
                app.get_profile_photos("me", limit=3, offset=5)
        """
        peer_id = await self.resolve_peer(chat_id)

        if isinstance(peer_id, raw.types.InputPeerChannel):
            r = await self.send(
                raw.functions.channels.GetFullChannel(
                    channel=peer_id
                )
            )

            current = types.Photo._parse(self, r.full_chat.chat_photo) or []

            r = await utils.parse_messages(
                self,
                await self.send(
                    raw.functions.messages.Search(
                        peer=peer_id,
                        q="",
                        filter=raw.types.InputMessagesFilterChatPhotos(),
                        min_date=0,
                        max_date=0,
                        offset_id=0,
                        add_offset=0,
                        limit=limit,
                        max_id=0,
                        min_id=0,
                        hash=0
                    )
                )
            )

            extra = [message.new_chat_photo for message in r]

            if extra:
                if current:
                    photos = ([current] + extra) if current.file_id != extra[0].file_id else extra
                else:
                    photos = extra
            else:
                if current:
                    photos = [current]
                else:
                    photos = []

            return types.List(photos[offset:limit])
        else:
            r = await self.send(
                raw.functions.photos.GetUserPhotos(
                    user_id=peer_id,
                    offset=offset,
                    max_id=0,
                    limit=limit
                )
            )

            return types.List(types.Photo._parse(self, photo) for photo in r.photos)

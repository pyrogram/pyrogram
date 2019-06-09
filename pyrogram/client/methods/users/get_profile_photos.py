# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

import pyrogram
from pyrogram.api import functions, types
from ...ext import BaseClient


class GetProfilePhotos(BaseClient):
    def get_profile_photos(
        self,
        chat_id: Union[int, str],
        offset: int = 0,
        limit: int = 100
    ) -> "pyrogram.ProfilePhotos":
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
            :obj:`ProfilePhotos`: On success, an object containing a list of the profile photos is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        peer_id = self.resolve_peer(chat_id)

        if isinstance(peer_id, (types.InputPeerUser, types.InputPeerSelf)):
            return pyrogram.ProfilePhotos._parse(
                self,
                self.send(
                    functions.photos.GetUserPhotos(
                        user_id=peer_id,
                        offset=offset,
                        max_id=0,
                        limit=limit
                    )
                )
            )
        else:
            new_chat_photos = pyrogram.Messages._parse(
                self,
                self.send(
                    functions.messages.Search(
                        peer=peer_id,
                        q="",
                        filter=types.InputMessagesFilterChatPhotos(),
                        min_date=0,
                        max_date=0,
                        offset_id=0,
                        add_offset=offset,
                        limit=limit,
                        max_id=0,
                        min_id=0,
                        hash=0
                    )
                )
            )

            return pyrogram.ProfilePhotos(
                total_count=new_chat_photos.total_count,
                profile_photos=[m.new_chat_photo for m in new_chat_photos.messages][:limit]
            )

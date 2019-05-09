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

import os
from base64 import b64decode
from struct import unpack
from typing import Union

from pyrogram.api import functions, types
from ...ext import BaseClient


class SetChatPhoto(BaseClient):
    def set_chat_photo(
        self,
        chat_id: Union[int, str],
        photo: str
    ) -> bool:
        """Use this method to set a new profile photo for the chat.
        Photos can't be changed for private chats.
        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Note:
            In regular groups (non-supergroups), this method will only work if the "All Members Are Admins"
            setting is off.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            photo (``str``):
                New chat photo. You can pass a :class:`Photo` id or a file path to upload a new photo.

        Returns:
            ``bool``: True on success.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ``ValueError`` if a chat_id belongs to user.
        """
        peer = self.resolve_peer(chat_id)

        if os.path.exists(photo):
            photo = types.InputChatUploadedPhoto(file=self.save_file(photo))
        else:
            s = unpack("<qq", b64decode(photo + "=" * (-len(photo) % 4), "-_"))

            photo = types.InputChatPhoto(
                id=types.InputPhoto(
                    id=s[0],
                    access_hash=s[1],
                    file_reference=b""
                )
            )

        if isinstance(peer, types.InputPeerChat):
            self.send(
                functions.messages.EditChatPhoto(
                    chat_id=peer.chat_id,
                    photo=photo
                )
            )
        elif isinstance(peer, types.InputPeerChannel):
            self.send(
                functions.channels.EditPhoto(
                    channel=peer,
                    photo=photo
                )
            )
        else:
            raise ValueError("The chat_id \"{}\" belongs to a user".format(chat_id))

        return True

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

import os
from typing import Union, BinaryIO

import pyrogram
from pyrogram import raw
from pyrogram import utils
from pyrogram.file_id import FileType


class SetChatPhoto:
    async def set_chat_photo(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        *,
        photo: Union[str, BinaryIO] = None,
        video: Union[str, BinaryIO] = None,
        video_start_ts: float = None,
    ) -> bool:
        """Set a new chat photo or video (H.264/MPEG-4 AVC video, max 5 seconds).

        The ``photo`` and ``video`` arguments are mutually exclusive.
        Pass either one as named argument (see examples below).

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            photo (``str`` | ``BinaryIO``, *optional*):
                New chat photo. You can pass a :obj:`~pyrogram.types.Photo` file_id, a file path to upload a new photo
                from your local machine or a binary file-like object with its attribute
                ".name" set for in-memory uploads.

            video (``str`` | ``BinaryIO``, *optional*):
                New chat video. You can pass a :obj:`~pyrogram.types.Video` file_id, a file path to upload a new video
                from your local machine or a binary file-like object with its attribute
                ".name" set for in-memory uploads.

            video_start_ts (``float``, *optional*):
                The timestamp in seconds of the video frame to use as photo profile preview.

        Returns:
            ``bool``: True on success.

        Raises:
            ValueError: if a chat_id belongs to user.

        Example:
            .. code-block:: python

                # Set chat photo using a local file
                await app.set_chat_photo(chat_id, photo="photo.jpg")

                # Set chat photo using an existing Photo file_id
                await app.set_chat_photo(chat_id, photo=photo.file_id)


                # Set chat video using a local file
                await app.set_chat_photo(chat_id, video="video.mp4")

                # Set chat photo using an existing Video file_id
                await app.set_chat_photo(chat_id, video=video.file_id)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(photo, str):
            if os.path.isfile(photo):
                photo = raw.types.InputChatUploadedPhoto(
                    file=await self.save_file(photo),
                    video=await self.save_file(video),
                    video_start_ts=video_start_ts,
                )
            else:
                photo = utils.get_input_media_from_file_id(photo, FileType.PHOTO)
                photo = raw.types.InputChatPhoto(id=photo.id)
        else:
            photo = raw.types.InputChatUploadedPhoto(
                file=await self.save_file(photo),
                video=await self.save_file(video),
                video_start_ts=video_start_ts,
            )

        if isinstance(peer, raw.types.InputPeerChat):
            await self.invoke(
                raw.functions.messages.EditChatPhoto(
                    chat_id=peer.chat_id,
                    photo=photo,
                )
            )
        elif isinstance(peer, raw.types.InputPeerChannel):
            await self.invoke(
                raw.functions.channels.EditPhoto(
                    channel=peer,
                    photo=photo
                )
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

        return True

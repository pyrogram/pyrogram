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

import asyncio
from io import IOBase
import os
import time
from datetime import datetime
from typing import AsyncGenerator, Union, Tuple

from pyrogram import types
from pyrogram.file_id import FileId
from pyrogram.scaffold import Scaffold


class IterDownloadMedia(Scaffold):
    async def iter_download_media(
        self,
        message: Union["types.Message", str]
    ) -> AsyncGenerator[Tuple[bytes, int, int], None]:
        """Download the media from a message.

        Parameters:
            message (:obj:`~pyrogram.types.Message` | ``str``):
                Pass a Message containing the media, the media itself (message.audio, message.video, ...) or a file id
                as string.

        Returns:
            ``AsyncGenerator`` Returns an asynchronous generator that yields tuples (chunk, current, total).

        Raises:
            ValueError: if the message doesn't contain any downloadable media

        Example:
            .. code-block:: python

                # Download from Message
                with open(file_name, 'wb') as f:
                    async for chunk, current, total in app.iter_download_media(message):
                        f.write(chunk)
                        print(f"{current * 100 / total:.1f}%")
        """
        available_media = ("audio", "document", "photo", "sticker", "animation", "video", "voice", "video_note",
                           "new_chat_photo")

        if isinstance(message, types.Message):
            for kind in available_media:
                media = getattr(message, kind, None)

                if media is not None:
                    break
            else:
                raise ValueError("This message doesn't contain any downloadable media")
        else:
            media = message

        if isinstance(media, str):
            file_id_str = media
        else:
            file_id_str = media.file_id

        file_id_obj = FileId.decode(file_id_str)
        file_size = getattr(media, "file_size", 0)

        return self.iter_handle_download((file_id_obj, file_size))

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

import asyncio
import binascii
import os
import struct
import time
from datetime import datetime
from typing import Union

from pyrogram import types
from pyrogram import utils
from pyrogram.errors import FileIdInvalid
from pyrogram.scaffold import Scaffold

DEFAULT_DOWNLOAD_DIR = "downloads/"


class FileData:
    def __init__(
        self, *, media_type: int = None, dc_id: int = None, document_id: int = None, access_hash: int = None,
        thumb_size: str = None, peer_id: int = None, peer_type: str = None, peer_access_hash: int = None,
        volume_id: int = None, local_id: int = None, is_big: bool = None, file_size: int = None, mime_type: str = None,
        file_name: str = None, date: int = None, file_ref: str = None
    ):
        self.media_type = media_type
        self.dc_id = dc_id
        self.document_id = document_id
        self.access_hash = access_hash
        self.thumb_size = thumb_size
        self.peer_id = peer_id
        self.peer_type = peer_type
        self.peer_access_hash = peer_access_hash
        self.volume_id = volume_id
        self.local_id = local_id
        self.is_big = is_big
        self.file_size = file_size
        self.mime_type = mime_type
        self.file_name = file_name
        self.date = date
        self.file_ref = file_ref


class DownloadMedia(Scaffold):
    async def download_media(
        self,
        message: Union["types.Message", str],
        file_ref: str = None,
        file_name: str = DEFAULT_DOWNLOAD_DIR,
        block: bool = True,
        progress: callable = None,
        progress_args: tuple = ()
    ) -> Union[str, None]:
        """Download the media from a message.

        Parameters:
            message (:obj:`~pyrogram.types.Message` | ``str``):
                Pass a Message containing the media, the media itself (message.audio, message.video, ...) or
                the file id as string.

            file_ref (``str``, *optional*):
                A valid file reference obtained by a recently fetched media message.
                To be used in combination with a file id in case a file reference is needed.

            file_name (``str``, *optional*):
                A custom *file_name* to be used instead of the one provided by Telegram.
                By default, all files are downloaded in the *downloads* folder in your working directory.
                You can also specify a path for downloading files in a custom location: paths that end with "/"
                are considered directories. All non-existent folders will be created automatically.

            block (``bool``, *optional*):
                Blocks the code execution until the file has been downloaded.
                Defaults to True.

            progress (``callable``, *optional*):
                Pass a callback function to view the file transmission progress.
                The function must take *(current, total)* as positional arguments (look at Other Parameters below for a
                detailed description) and will be called back each time a new file chunk has been successfully
                transmitted.

            progress_args (``tuple``, *optional*):
                Extra custom arguments for the progress callback function.
                You can pass anything you need to be available in the progress callback scope; for example, a Message
                object or a Client instance in order to edit the message with the updated progress status.

        Other Parameters:
            current (``int``):
                The amount of bytes transmitted so far.

            total (``int``):
                The total size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the ``progress_args`` parameter.
                You can either keep ``*args`` or add every single extra argument in your function signature.

        Returns:
            ``str`` | ``None``: On success, the absolute path of the downloaded file is returned, otherwise, in case
            the download failed or was deliberately stopped with :meth:`~pyrogram.Client.stop_transmission`, None is
            returned.

        Raises:
            ValueError: if the message doesn't contain any downloadable media

        Example:
            .. code-block:: python

                # Download from Message
                app.download_media(message)

                # Download from file id
                app.download_media("CAADBAADzg4AAvLQYAEz_x2EOgdRwBYE")

                # Keep track of the progress while downloading
                def progress(current, total):
                    print(f"{current * 100 / total:.1f}%")

                app.download_media(message, progress=progress)
        """
        error_message = "This message doesn't contain any downloadable media"
        available_media = ("audio", "document", "photo", "sticker", "animation", "video", "voice", "video_note")

        media_file_name = None
        file_size = None
        mime_type = None
        date = None

        if isinstance(message, types.Message):
            for kind in available_media:
                media = getattr(message, kind, None)

                if media is not None:
                    break
            else:
                raise ValueError(error_message)
        else:
            media = message

        if isinstance(media, str):
            file_id_str = media
        else:
            file_id_str = media.file_id
            media_file_name = getattr(media, "file_name", "")
            file_size = getattr(media, "file_size", None)
            mime_type = getattr(media, "mime_type", None)
            date = getattr(media, "date", None)
            file_ref = getattr(media, "file_ref", None)

        data = FileData(
            file_name=media_file_name,
            file_size=file_size,
            mime_type=mime_type,
            date=date,
            file_ref=file_ref
        )

        def get_existing_attributes() -> dict:
            return dict(filter(lambda x: x[1] is not None, data.__dict__.items()))

        try:
            decoded = utils.decode_file_id(file_id_str)
            media_type = decoded[0]

            if media_type == 1:
                unpacked = struct.unpack("<iiqqqiiiqi", decoded)
                dc_id, photo_id, _, volume_id, size_type, peer_id, x, peer_access_hash, local_id = unpacked[1:]

                if x == 0:
                    peer_type = "user"
                elif x == -1:
                    peer_id = -peer_id
                    peer_type = "chat"
                else:
                    peer_id = utils.get_channel_id(peer_id - 1000727379968)
                    peer_type = "channel"

                data = FileData(
                    **get_existing_attributes(),
                    media_type=media_type,
                    dc_id=dc_id,
                    peer_id=peer_id,
                    peer_type=peer_type,
                    peer_access_hash=peer_access_hash,
                    volume_id=volume_id,
                    local_id=local_id,
                    is_big=size_type == 3
                )
            elif media_type in (0, 2, 14):
                unpacked = struct.unpack("<iiqqqiiii", decoded)
                dc_id, document_id, access_hash, volume_id, _, _, thumb_size, local_id = unpacked[1:]

                data = FileData(
                    **get_existing_attributes(),
                    media_type=media_type,
                    dc_id=dc_id,
                    document_id=document_id,
                    access_hash=access_hash,
                    thumb_size=chr(thumb_size)
                )
            elif media_type in (3, 4, 5, 8, 9, 10, 13):
                unpacked = struct.unpack("<iiqq", decoded)
                dc_id, document_id, access_hash = unpacked[1:]

                data = FileData(
                    **get_existing_attributes(),
                    media_type=media_type,
                    dc_id=dc_id,
                    document_id=document_id,
                    access_hash=access_hash
                )
            else:
                raise ValueError(f"Unknown media type: {file_id_str}")
        except (AssertionError, binascii.Error, struct.error):
            raise FileIdInvalid from None

        directory, file_name = os.path.split(file_name)
        file_name = file_name or data.file_name or ""

        if not os.path.isabs(file_name):
            directory = self.PARENT_DIR / (directory or DEFAULT_DOWNLOAD_DIR)

        media_type_str = self.MEDIA_TYPE_ID[data.media_type]

        if not file_name:
            guessed_extension = self.guess_extension(data.mime_type)

            if data.media_type in (0, 1, 2, 14):
                extension = ".jpg"
            elif data.media_type == 3:
                extension = guessed_extension or ".ogg"
            elif data.media_type in (4, 10, 13):
                extension = guessed_extension or ".mp4"
            elif data.media_type == 5:
                extension = guessed_extension or ".zip"
            elif data.media_type == 8:
                extension = guessed_extension or ".webp"
            elif data.media_type == 9:
                extension = guessed_extension or ".mp3"
            else:
                extension = ".unknown"

            file_name = "{}_{}_{}{}".format(
                media_type_str,
                datetime.fromtimestamp(data.date or time.time()).strftime("%Y-%m-%d_%H-%M-%S"),
                self.rnd_id(),
                extension
            )

        downloader = self.handle_download((data, directory, file_name, progress, progress_args))

        if block:
            return await downloader
        else:
            asyncio.get_event_loop().create_task(downloader)

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

from threading import Event
from typing import Union

import pyrogram
from pyrogram.client.ext import BaseClient


class DownloadMedia(BaseClient):
    def download_media(self,
                       message: Union["pyrogram.Message", str],
                       file_name: str = "",
                       block: bool = True,
                       progress: callable = None,
                       progress_args: tuple = ()) -> Union[str, None]:
        """Use this method to download the media from a Message.

        Args:
            message (:obj:`Message <pyrogram.Message>` | ``str``):
                Pass a Message containing the media, the media itself (message.audio, message.video, ...) or
                the file id as string.

            file_name (``str``, *optional*):
                A custom *file_name* to be used instead of the one provided by Telegram.
                By default, all files are downloaded in the *downloads* folder in your working directory.
                You can also specify a path for downloading files in a custom location: paths that end with "/"
                are considered directories. All non-existent folders will be created automatically.

            block (``bool``, *optional*):
                Blocks the code execution until the file has been downloaded.
                Defaults to True.

            progress (``callable``):
                Pass a callback function to view the download progress.
                The function must take *(client, current, total, \*args)* as positional arguments (look at the section
                below for a detailed description).

            progress_args (``tuple``):
                Extra custom arguments for the progress callback function. Useful, for example, if you want to pass
                a chat_id and a message_id in order to edit a message with the updated progress.

        Other Parameters:
            client (:obj:`Client <pyrogram.Client>`):
                The Client itself, useful when you want to call other API methods inside the callback function.

            current (``int``):
                The amount of bytes downloaded so far.

            total (``int``):
                The size of the file.

            *args (``tuple``, *optional*):
                Extra custom arguments as defined in the *progress_args* parameter.
                You can either keep *\*args* or add every single extra argument in your function signature.

        Returns:
            On success, the absolute path of the downloaded file as string is returned, None otherwise.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
            ``ValueError`` if the message doesn't contain any downloadable media
        """
        error_message = "This message doesn't contain any downloadable media"

        if isinstance(message, pyrogram.Message):
            if message.photo:
                media = pyrogram.Document(
                    file_id=message.photo.sizes[-1].file_id,
                    file_size=message.photo.sizes[-1].file_size,
                    mime_type="",
                    date=message.photo.date,
                    client=self
                )
            elif message.audio:
                media = message.audio
            elif message.document:
                media = message.document
            elif message.video:
                media = message.video
            elif message.voice:
                media = message.voice
            elif message.video_note:
                media = message.video_note
            elif message.sticker:
                media = message.sticker
            elif message.animation:
                media = message.animation
            else:
                raise ValueError(error_message)
        elif isinstance(message, (
                pyrogram.Photo,
                pyrogram.PhotoSize,
                pyrogram.Audio,
                pyrogram.Document,
                pyrogram.Video,
                pyrogram.Voice,
                pyrogram.VideoNote,
                pyrogram.Sticker,
                pyrogram.Animation
        )):
            if isinstance(message, pyrogram.Photo):
                media = pyrogram.Document(
                    file_id=message.sizes[-1].file_id,
                    file_size=message.sizes[-1].file_size,
                    mime_type="",
                    date=message.date,
                    client=self
                )
            else:
                media = message
        elif isinstance(message, str):
            media = pyrogram.Document(
                file_id=message,
                file_size=0,
                mime_type="",
                client=self
            )
        else:
            raise ValueError(error_message)

        done = Event()
        path = [None]

        self.download_queue.put((media, file_name, done, progress, progress_args, path))

        if block:
            done.wait()

        return path[0]

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

from struct import pack
from typing import List

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram.utils import encode_file_id, encode_file_ref
from ..object import Object


class Audio(Object):
    """An audio file to be treated as music by the Telegram clients.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        file_ref (``str``):
            Up to date file reference.

        duration (``int``):
            Duration of the audio in seconds as defined by sender.

        file_name (``str``, *optional*):
            Audio file name.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the audio was sent in Unix time.

        performer (``str``, *optional*):
            Performer of the audio as defined by sender or by audio tags.

        title (``str``, *optional*):
            Title of the audio as defined by sender or by audio tags.

        thumbs (List of :obj:`~pyrogram.types.Thumbnail`, *optional*):
            Thumbnails of the music file album cover.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_ref: str,
        duration: int,
        file_name: str = None,
        mime_type: str = None,
        file_size: int = None,
        date: int = None,
        performer: str = None,
        title: str = None,
        thumbs: List["types.Thumbnail"] = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.duration = duration
        self.performer = performer
        self.title = title
        self.thumbs = thumbs

    @staticmethod
    def _parse(
        client,
        audio: "raw.types.Document",
        audio_attributes: "raw.types.DocumentAttributeAudio",
        file_name: str
    ) -> "Audio":
        return Audio(
            file_id=encode_file_id(
                pack(
                    "<iiqq",
                    9,
                    audio.dc_id,
                    audio.id,
                    audio.access_hash
                )
            ),
            file_ref=encode_file_ref(audio.file_reference),
            duration=audio_attributes.duration,
            performer=audio_attributes.performer,
            title=audio_attributes.title,
            mime_type=audio.mime_type,
            file_size=audio.size,
            file_name=file_name,
            date=audio.date,
            thumbs=types.Thumbnail._parse(client, audio),
            client=client
        )

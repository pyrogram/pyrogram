# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

from struct import pack

from pyrogram.api import types
from .photo_size import PhotoSize
from ..pyrogram_type import PyrogramType
from ...ext.utils import encode


class Audio(PyrogramType):
    """This object represents an audio file to be treated as music by the Telegram clients.

    Args:
        file_id (``str``):
            Unique identifier for this file.

        duration (``int``):
            Duration of the audio in seconds as defined by sender.

        thumb (:obj:`PhotoSize <pyrogram.PhotoSize>`, *optional*):
            Thumbnail of the music file album cover.

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
    """

    def __init__(self,
                 *,
                 client,
                 file_id: str,
                 duration: int,
                 thumb=None,
                 file_name: str = None,
                 mime_type: str = None,
                 file_size: int = None,
                 date: int = None,
                 performer: str = None,
                 title: str = None):
        super().__init__(client)

        self.file_id = file_id
        self.thumb = thumb
        self.file_name = file_name
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date
        self.duration = duration
        self.performer = performer
        self.title = title

    @staticmethod
    def _parse(client, audio: types.Document, audio_attributes: types.DocumentAttributeAudio, file_name: str) -> "Audio":
        return Audio(
            file_id=encode(
                pack(
                    "<iiqq",
                    9,
                    audio.dc_id,
                    audio.id,
                    audio.access_hash
                )
            ),
            duration=audio_attributes.duration,
            performer=audio_attributes.performer,
            title=audio_attributes.title,
            mime_type=audio.mime_type,
            file_size=audio.size,
            thumb=PhotoSize._parse(client, audio.thumb),
            file_name=file_name,
            date=audio.date,
            client=client
        )

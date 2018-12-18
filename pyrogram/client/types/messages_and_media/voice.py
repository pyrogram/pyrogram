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
from ..pyrogram_type import PyrogramType
from ...ext.utils import encode


class Voice(PyrogramType):
    """This object represents a voice note.

    Args:
        file_id (``str``):
            Unique identifier for this file.

        duration (``int``):
            Duration of the audio in seconds as defined by sender.

        waveform (``bytes``, *optional*):
            Voice waveform.

        mime_type (``str``, *optional*):
            MIME type of the file as defined by sender.

        file_size (``int``, *optional*):
            File size.

        date (``int``, *optional*):
            Date the voice was sent in Unix time.
    """

    def __init__(self, *, client, file_id: str, duration: int, waveform: bytes = None, mime_type: str = None,
                 file_size: int = None, date: int = None):
        super().__init__(client)

        self.file_id = file_id
        self.duration = duration
        self.waveform = waveform
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date

    @staticmethod
    def parse(client, voice: types.Document, attributes: types.DocumentAttributeAudio) -> "Voice":
        return Voice(
            file_id=encode(
                pack(
                    "<iiqq",
                    3,
                    voice.dc_id,
                    voice.id,
                    voice.access_hash
                )
            ),
            duration=attributes.duration,
            mime_type=voice.mime_type,
            file_size=voice.size,
            waveform=attributes.waveform,
            date=voice.date,
            client=client
        )

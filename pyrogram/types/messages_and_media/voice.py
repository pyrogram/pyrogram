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

import pyrogram
from pyrogram import raw
from pyrogram.utils import encode_file_id, encode_file_ref
from ..object import Object


class Voice(Object):
    """A voice note.

    Parameters:
        file_id (``str``):
            Unique identifier for this file.

        file_ref (``str``):
            Up to date file reference.

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

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        file_id: str,
        file_ref: str,
        duration: int,
        waveform: bytes = None,
        mime_type: str = None,
        file_size: int = None,
        date: int = None
    ):
        super().__init__(client)

        self.file_id = file_id
        self.file_ref = file_ref
        self.duration = duration
        self.waveform = waveform
        self.mime_type = mime_type
        self.file_size = file_size
        self.date = date

    @staticmethod
    def _parse(client, voice: "raw.types.Document", attributes: "raw.types.DocumentAttributeAudio") -> "Voice":
        return Voice(
            file_id=encode_file_id(
                pack(
                    "<iiqq",
                    3,
                    voice.dc_id,
                    voice.id,
                    voice.access_hash
                )
            ),
            file_ref=encode_file_ref(voice.file_reference),
            duration=attributes.duration,
            mime_type=voice.mime_type,
            file_size=voice.size,
            waveform=attributes.waveform,
            date=voice.date,
            client=client
        )

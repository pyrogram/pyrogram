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

from typing import List

import pyrogram
from pyrogram import raw
from ..object import Object


class WebDocument(Object):
    """A remote document.

    Parameters:
        url (``str``):
            Unique identifier for this file.

        mime_type (``str``):
            Duration of the audio in seconds as defined by sender.

        file_size (``int``):
            Up to date file reference.

        attributes (List of :obj:`~pyrogram.raw.types.DocumentAttributeImageSize`):
            Voice waveform.
    """

    def __init__(
        self,
        *,
        client: "pyrogram.Client" = None,
        url: str,
        mime_type: str,
        file_size: int,
        attributes: List["raw.base.DocumentAttribute"]
    ):
        super().__init__(client)

        self.url = url
        self.mime_type = mime_type
        self.file_size = file_size
        self.attributes = attributes

    @staticmethod
    def _parse(client, web_document: "raw.types.WebDocument") -> "WebDocument":
        return WebDocument(
            url=web_document.url,
            mime_type=web_document.mime_type,
            file_size=web_document.size,
            attributes=web_document.attributes,
            client=client
        )

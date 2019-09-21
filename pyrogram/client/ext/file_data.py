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


class FileData:
    def __init__(
        self, *, media_type: int = None, dc_id: int = None, document_id: int = None, access_hash: int = None,
        thumb_size: str = None, peer_id: int = None, peer_access_hash: int = None, volume_id: int = None,
        local_id: int = None, is_big: bool = None, file_size: int = None, mime_type: str = None, file_name: str = None,
        date: int = None, file_ref: bytes = None
    ):
        self.media_type = media_type
        self.dc_id = dc_id
        self.document_id = document_id
        self.access_hash = access_hash
        self.thumb_size = thumb_size
        self.peer_id = peer_id
        self.peer_access_hash = peer_access_hash
        self.volume_id = volume_id
        self.local_id = local_id
        self.is_big = is_big
        self.file_size = file_size
        self.mime_type = mime_type
        self.file_name = file_name
        self.date = date
        self.file_ref = file_ref

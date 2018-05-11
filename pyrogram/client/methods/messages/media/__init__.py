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

from .send_audio import SendAudio
from .send_contact import SendContact
from .send_document import SendDocument
from .send_gif import SendGIF
from .send_location import SendLocation
from .send_media_group import SendMediaGroup
from .send_photo import SendPhoto
from .send_sticker import SendSticker
from .send_venue import SendVenue
from .send_video import SendVideo
from .send_video_note import SendVideoNote
from .send_voice import SendVoice


class Media(
    SendContact,
    SendVenue,
    SendLocation,
    SendMediaGroup,
    SendVideoNote,
    SendVoice,
    SendVideo,
    SendGIF,
    SendSticker,
    SendDocument,
    SendAudio,
    SendPhoto
):
    pass

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

from .delete_messages import DeleteMessages
from .edit_message_caption import EditMessageCaption
from .edit_message_reply_markup import EditMessageReplyMarkup
from .edit_message_text import EditMessageText
from .forward_messages import ForwardMessages
from .get_history import GetHistory
from .get_messages import GetMessages
from .send_audio import SendAudio
from .send_chat_action import SendChatAction
from .send_contact import SendContact
from .send_document import SendDocument
from .send_gif import SendGIF
from .send_location import SendLocation
from .send_media_group import SendMediaGroup
from .send_message import SendMessage
from .send_photo import SendPhoto
from .send_sticker import SendSticker
from .send_venue import SendVenue
from .send_video import SendVideo
from .send_video_note import SendVideoNote
from .send_voice import SendVoice


class Messages(
    DeleteMessages,
    EditMessageCaption,
    EditMessageReplyMarkup,
    EditMessageText,
    ForwardMessages,
    GetHistory,
    GetMessages,
    SendAudio,
    SendChatAction,
    SendContact,
    SendDocument,
    SendGIF,
    SendLocation,
    SendMediaGroup,
    SendMessage,
    SendPhoto,
    SendSticker,
    SendVenue,
    SendVideo,
    SendVideoNote,
    SendVoice
):
    pass

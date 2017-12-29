# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017 Dan Tès <https://github.com/delivrance>
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

from pyrogram.api import types


class ChatAction:
    """This class provides constants to be used for sending Chat Actions"""

    CANCEL = types.SendMessageCancelAction
    TYPING = types.SendMessageTypingAction
    PLAYING = types.SendMessageGamePlayAction
    CHOOSE_CONTACT = types.SendMessageChooseContactAction
    UPLOAD_PHOTO = types.SendMessageUploadPhotoAction
    RECORD_VIDEO = types.SendMessageRecordVideoAction
    UPLOAD_VIDEO = types.SendMessageUploadVideoAction
    RECORD_AUDIO = types.SendMessageRecordAudioAction
    UPLOAD_AUDIO = types.SendMessageUploadAudioAction
    UPLOAD_DOCUMENT = types.SendMessageUploadDocumentAction
    FIND_LOCATION = types.SendMessageGeoLocationAction
    RECORD_VIDEO_NOTE = types.SendMessageRecordRoundAction
    UPLOAD_VIDEO_NOTE = types.SendMessageUploadRoundAction

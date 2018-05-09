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

from enum import Enum

from pyrogram.api import types


class ChatAction(Enum):
    """This enumeration provides a convenient access to all Chat Actions available.
    Chat Actions are intended to be used with
    :meth:`send_chat_action() <pyrogram.Client.send_chat_action>`.
    """

    CANCEL = types.SendMessageCancelAction
    """Cancels any chat action currently displayed."""

    TYPING = types.SendMessageTypingAction
    """User is typing a text message."""

    PLAYING = types.SendMessageGamePlayAction
    """User is playing a game."""

    CHOOSE_CONTACT = types.SendMessageChooseContactAction
    """User is choosing a contact to share."""

    UPLOAD_PHOTO = types.SendMessageUploadPhotoAction
    """User is uploading a photo."""

    RECORD_VIDEO = types.SendMessageRecordVideoAction
    """User is recording a video."""

    UPLOAD_VIDEO = types.SendMessageUploadVideoAction
    """User is uploading a video."""

    RECORD_AUDIO = types.SendMessageRecordAudioAction
    """User is recording an audio message."""

    UPLOAD_AUDIO = types.SendMessageUploadAudioAction
    """User is uploading an audio message."""

    UPLOAD_DOCUMENT = types.SendMessageUploadDocumentAction
    """User is uploading a generic document."""

    FIND_LOCATION = types.SendMessageGeoLocationAction
    """User is searching for a location on the map."""

    RECORD_VIDEO_NOTE = types.SendMessageRecordRoundAction
    """User is recording a round video note."""

    UPLOAD_VIDEO_NOTE = types.SendMessageUploadRoundAction
    """User is uploading a round video note."""

    @staticmethod
    def from_string(action: str) -> "ChatAction":
        for a in ChatAction:
            if a.name.lower() == action.lower():
                return a

        raise ValueError("Invalid ChatAction: '{}'. Possible types are {}".format(
            action, [x.name.lower() for x in ChatAction]
        ))

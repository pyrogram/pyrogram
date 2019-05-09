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

from typing import Union

from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient
import json


class ChatAction:
    TYPING = types.SendMessageTypingAction
    UPLOAD_PHOTO = types.SendMessageUploadPhotoAction
    RECORD_VIDEO = types.SendMessageRecordVideoAction
    UPLOAD_VIDEO = types.SendMessageUploadVideoAction
    RECORD_AUDIO = types.SendMessageRecordAudioAction
    UPLOAD_AUDIO = types.SendMessageUploadAudioAction
    UPLOAD_DOCUMENT = types.SendMessageUploadDocumentAction
    FIND_LOCATION = types.SendMessageGeoLocationAction
    RECORD_VIDEO_NOTE = types.SendMessageRecordRoundAction
    UPLOAD_VIDEO_NOTE = types.SendMessageUploadRoundAction
    PLAYING = types.SendMessageGamePlayAction
    CHOOSE_CONTACT = types.SendMessageChooseContactAction
    CANCEL = types.SendMessageCancelAction


POSSIBLE_VALUES = list(map(lambda x: x.lower(), filter(lambda x: not x.startswith("__"), ChatAction.__dict__.keys())))


class SendChatAction(BaseClient):
    def send_chat_action(self, chat_id: Union[int, str], action: str) -> bool:
        """Use this method when you need to tell the other party that something is happening on your side.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            action (``str``):
                Type of action to broadcast. Choose one, depending on what the user is about to receive: *"typing"* for
                text messages, *"upload_photo"* for photos, *"record_video"* or *"upload_video"* for videos,
                *"record_audio"* or *"upload_audio"* for audio files, *"upload_document"* for general files,
                *"find_location"* for location data, *"record_video_note"* or *"upload_video_note"* for video notes,
                *"choose_contact"* for contacts, *"playing"* for games or *"cancel"* to cancel any chat action currently
                displayed.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
            ValueError: In case the provided string is not a valid ChatAction.
        """

        try:
            action = ChatAction.__dict__[action.upper()]
        except KeyError:
            raise ValueError("Invalid chat action '{}'. Possible values are: {}".format(
                action, json.dumps(POSSIBLE_VALUES, indent=4))) from None

        if "Upload" in action.__name__:
            action = action(progress=0)
        else:
            action = action()

        return self.send(
            functions.messages.SetTyping(
                peer=self.resolve_peer(chat_id),
                action=action
            )
        )

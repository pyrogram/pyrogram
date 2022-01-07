#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
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

import json
from typing import Union

from pyrogram import raw
from pyrogram.scaffold import Scaffold


class ChatAction:
    TYPING = raw.types.SendMessageTypingAction
    UPLOAD_PHOTO = raw.types.SendMessageUploadPhotoAction
    RECORD_VIDEO = raw.types.SendMessageRecordVideoAction
    UPLOAD_VIDEO = raw.types.SendMessageUploadVideoAction
    RECORD_AUDIO = raw.types.SendMessageRecordAudioAction
    UPLOAD_AUDIO = raw.types.SendMessageUploadAudioAction
    UPLOAD_DOCUMENT = raw.types.SendMessageUploadDocumentAction
    FIND_LOCATION = raw.types.SendMessageGeoLocationAction
    RECORD_VIDEO_NOTE = raw.types.SendMessageRecordRoundAction
    UPLOAD_VIDEO_NOTE = raw.types.SendMessageUploadRoundAction
    PLAYING = raw.types.SendMessageGamePlayAction
    CHOOSE_CONTACT = raw.types.SendMessageChooseContactAction
    SPEAKING = raw.types.SpeakingInGroupCallAction
    IMPORT_HISTORY = raw.types.SendMessageHistoryImportAction
    CHOOSE_STICKER = raw.types.SendMessageChooseStickerAction
    CANCEL = raw.types.SendMessageCancelAction


POSSIBLE_VALUES = list(map(lambda x: x.lower(), filter(lambda x: not x.startswith("__"), ChatAction.__dict__.keys())))


class SendChatAction(Scaffold):
    async def send_chat_action(self, chat_id: Union[int, str], action: str) -> bool:
        """Tell the other party that something is happening on your side.

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
                *"choose_contact"* for contacts, *"playing"* for games, *"speaking"* for speaking in group calls or
                *"import_history"* for importing history, *"choose_sticker"* for stickers or
                *"cancel"* to cancel any chat action currently displayed.

        Returns:
            ``bool``: On success, True is returned.

        Raises:
            ValueError: In case the provided string is not a valid chat action.

        Example:
            .. code-block:: python

                # Send "typing" chat action
                app.send_chat_action(chat_id, "typing")

                # Send "upload_video" chat action
                app.send_chat_action(chat_id, "upload_video")

                # Send "playing" chat action
                app.send_chat_action(chat_id, "playing")

                # Cancel any current chat action
                app.send_chat_action(chat_id, "cancel")
        """

        try:
            action = ChatAction.__dict__[action.upper()]
        except KeyError:
            raise ValueError("Invalid chat action '{}'. Possible values are: {}".format(
                action, json.dumps(POSSIBLE_VALUES, indent=4))) from None

        if "Upload" in action.__name__ or "History" in action.__name__:
            action = action(progress=0)
        else:
            action = action()

        return await self.send(
            raw.functions.messages.SetTyping(
                peer=await self.resolve_peer(chat_id),
                action=action
            )
        )

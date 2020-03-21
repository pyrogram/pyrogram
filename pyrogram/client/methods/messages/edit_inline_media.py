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

import pyrogram
from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient, utils
from pyrogram.client.types import (
    InputMediaPhoto, InputMediaVideo, InputMediaAudio,
    InputMediaAnimation, InputMediaDocument
)
from pyrogram.client.types.input_media import InputMedia


class EditInlineMedia(BaseClient):
    def edit_inline_media(
        self,
        inline_message_id: str,
        media: InputMedia,
        reply_markup: "pyrogram.InlineKeyboardMarkup" = None
    ) -> bool:
        """Edit inline animation, audio, document, photo or video messages.

        When the inline message is edited, a new file can't be uploaded. Use a previously uploaded file via its file_id
        or specify a URL.

        Parameters:
            inline_message_id (``str``):
                Required if *chat_id* and *message_id* are not specified.
                Identifier of the inline message.

            media (:obj:`InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from pyrogram import InputMediaPhoto, InputMediaVideo, InputMediaAudio

                # Bots only

                # Replace the current media with a local photo
                app.edit_inline_media(inline_message_id, InputMediaPhoto("new_photo.jpg"))

                # Replace the current media with a local video
                app.edit_inline_media(inline_message_id, InputMediaVideo("new_video.mp4"))

                # Replace the current media with a local audio
                app.edit_inline_media(inline_message_id, InputMediaAudio("new_audio.mp3"))
        """
        caption = media.caption
        parse_mode = media.parse_mode

        if isinstance(media, InputMediaPhoto):
            if media.media.startswith("http"):
                media = types.InputMediaPhotoExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, media.file_ref, 2)
        elif isinstance(media, InputMediaVideo):
            if media.media.startswith("http"):
                media = types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, media.file_ref, 4)
        elif isinstance(media, InputMediaAudio):
            if media.media.startswith("http"):
                media = types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, media.file_ref, 9)
        elif isinstance(media, InputMediaAnimation):
            if media.media.startswith("http"):
                media = types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, media.file_ref, 10)
        elif isinstance(media, InputMediaDocument):
            if media.media.startswith("http"):
                media = types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, media.file_ref, 5)

        return self.send(
            functions.messages.EditInlineBotMessage(
                id=utils.unpack_inline_message_id(inline_message_id),
                media=media,
                reply_markup=reply_markup.write() if reply_markup else None,
                **self.parser.parse(caption, parse_mode)
            )
        )

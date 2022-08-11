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

import os
import re
import asyncio
import io

import pyrogram
from pyrogram import raw
from pyrogram import types
from pyrogram import utils
from pyrogram.errors import RPCError, MediaEmpty
from pyrogram.file_id import FileType
from .inline_session import get_session


class EditInlineMedia:
    MAX_RETRIES = 3

    async def edit_inline_media(
        self: "pyrogram.Client",
        inline_message_id: str,
        media: "types.InputMedia",
        reply_markup: "types.InlineKeyboardMarkup" = None
    ) -> bool:
        """Edit inline animation, audio, document, photo or video messages.

        When the inline message is edited, a new file can't be uploaded. Use a previously uploaded file via its file_id
        or specify a URL.

        Parameters:
            inline_message_id (``str``):
                Required if *chat_id* and *message_id* are not specified.
                Identifier of the inline message.

            media (:obj:`~pyrogram.types.InputMedia`):
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            ``bool``: On success, True is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import InputMediaPhoto, InputMediaVideo, InputMediaAudio

                # Bots only

                # Replace the current media with a local photo
                await app.edit_inline_media(inline_message_id, InputMediaPhoto("new_photo.jpg"))

                # Replace the current media with a local video
                await app.edit_inline_media(inline_message_id, InputMediaVideo("new_video.mp4"))

                # Replace the current media with a local audio
                await app.edit_inline_media(inline_message_id, InputMediaAudio("new_audio.mp3"))
        """
        caption = media.caption
        parse_mode = media.parse_mode

        if isinstance(media, types.InputMediaPhoto):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                media = raw.types.InputMediaUploadedPhoto(
                    file=await self.save_file(media.media)
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaPhotoExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.PHOTO)
        elif isinstance(media, types.InputMediaVideo):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(media.media) or "video/mp4",
                    thumb=await self.save_file(media.thumb),
                    file=await self.save_file(media.media),
                    attributes=[
                        raw.types.DocumentAttributeVideo(
                            supports_streaming=media.supports_streaming or None,
                            duration=media.duration,
                            w=media.width,
                            h=media.height
                        ),
                        raw.types.DocumentAttributeFilename(
                            file_name=os.path.basename(media.media)
                        )
                    ]
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.VIDEO)
        elif isinstance(media, types.InputMediaAudio):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(media.media) or "audio/mpeg",
                    thumb=await self.save_file(media.thumb),
                    file=await self.save_file(media.media),
                    attributes=[
                        raw.types.DocumentAttributeAudio(
                            duration=media.duration,
                            performer=media.performer,
                            title=media.title
                        ),
                        raw.types.DocumentAttributeFilename(
                            file_name=os.path.basename(media.media)
                        )
                    ]
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.AUDIO)
        elif isinstance(media, types.InputMediaAnimation):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(media.media) or "video/mp4",
                    thumb=await self.save_file(media.thumb),
                    file=await self.save_file(media.media),
                    attributes=[
                        raw.types.DocumentAttributeVideo(
                            supports_streaming=True,
                            duration=media.duration,
                            w=media.width,
                            h=media.height
                        ),
                        raw.types.DocumentAttributeFilename(
                            file_name=os.path.basename(media.media)
                        ),
                        raw.types.DocumentAttributeAnimated()
                    ],
                    nosound_video=True
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.ANIMATION)
        elif isinstance(media, types.InputMediaDocument):
            if isinstance(media.media, io.BytesIO) or os.path.isfile(media.media):
                media = raw.types.InputMediaUploadedDocument(
                    mime_type=self.guess_mime_type(media.media) or "application/zip",
                    thumb=await self.save_file(media.thumb),
                    file=await self.save_file(media.media),
                    attributes=[
                        raw.types.DocumentAttributeFilename(
                            file_name=os.path.basename(media.media)
                        )
                    ],
                    force_file=True
                )
            elif re.match("^https?://", media.media):
                media = raw.types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, FileType.DOCUMENT)

        unpacked = utils.unpack_inline_message_id(inline_message_id)
        dc_id = unpacked.dc_id

        session = await get_session(self, dc_id)

        actual_media = await self.invoke(
            raw.functions.messages.UploadMedia(
                peer=raw.types.InputPeerSelf(),
                media=media
            )
        )

        for i in range(self.MAX_RETRIES):
            try:
                return await session.invoke(
                    raw.functions.messages.EditInlineBotMessage(
                        id=unpacked,
                        media=raw.types.InputMediaDocument(
                            id=raw.types.InputDocument(
                                id=actual_media.document.id,
                                access_hash=actual_media.document.access_hash,
                                file_reference=actual_media.document.file_reference
                            )
                        ),
                        reply_markup=await reply_markup.write(self) if reply_markup else None,
                        **await self.parser.parse(caption, parse_mode)
                    ),
                    sleep_threshold=self.sleep_threshold
                )
            except RPCError as e:
                if i == self.MAX_RETRIES - 1:
                    raise

                if isinstance(e, MediaEmpty):
                    # Must wait due to a server race condition
                    await asyncio.sleep(1)

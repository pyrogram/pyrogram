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

import os
from typing import Union

import pyrogram
from pyrogram.api import functions, types
from pyrogram.client.ext import BaseClient, utils
from pyrogram.client.types import (
    InputMediaPhoto, InputMediaVideo, InputMediaAudio,
    InputMediaAnimation, InputMediaDocument
)
from pyrogram.client.types.input_media import InputMedia


class EditMessageMedia(BaseClient):
    def edit_message_media(
        self,
        chat_id: Union[int, str],
        message_id: int,
        media: InputMedia,
        reply_markup: "pyrogram.InlineKeyboardMarkup" = None
    ) -> "pyrogram.Message":
        """Edit audio, document, photo, or video messages.

        If a message is a part of a message album, then it can be edited only to a photo or a video. Otherwise,
        message type can be changed arbitrarily. When inline message is edited, new file can't be uploaded.
        Use previously uploaded file via its file_id or specify a URL. On success, if the edited message was sent
        by the bot, the edited Message is returned, otherwise True is returned.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            media (:obj:`InputMedia`)
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            :obj:`Message`: On success, the edited message is returned.

        Raises:
            RPCError: In case of a Telegram RPC error.
        """
        style = self.html if media.parse_mode.lower() == "html" else self.markdown
        caption = media.caption

        if isinstance(media, InputMediaPhoto):
            if os.path.exists(media.media):
                media = self.send(
                    functions.messages.UploadMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedPhoto(
                            file=self.save_file(media.media)
                        )
                    )
                )

                media = types.InputMediaPhoto(
                    id=types.InputPhoto(
                        id=media.photo.id,
                        access_hash=media.photo.access_hash,
                        file_reference=b""
                    )
                )
            elif media.media.startswith("http"):
                media = types.InputMediaPhotoExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, 2)

        if isinstance(media, InputMediaVideo):
            if os.path.exists(media.media):
                media = self.send(
                    functions.messages.UploadMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "video/mp4",
                            thumb=None if media.thumb is None else self.save_file(media.thumb),
                            file=self.save_file(media.media),
                            attributes=[
                                types.DocumentAttributeVideo(
                                    supports_streaming=media.supports_streaming or None,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height
                                ),
                                types.DocumentAttributeFilename(
                                    file_name=os.path.basename(media.media)
                                )
                            ]
                        )
                    )
                )

                media = types.InputMediaDocument(
                    id=types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=b""
                    )
                )
            elif media.media.startswith("http"):
                media = types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, 4)

        if isinstance(media, InputMediaAudio):
            if os.path.exists(media.media):
                media = self.send(
                    functions.messages.UploadMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "audio/mpeg",
                            thumb=None if media.thumb is None else self.save_file(media.thumb),
                            file=self.save_file(media.media),
                            attributes=[
                                types.DocumentAttributeAudio(
                                    duration=media.duration,
                                    performer=media.performer,
                                    title=media.title
                                ),
                                types.DocumentAttributeFilename(
                                    file_name=os.path.basename(media.media)
                                )
                            ]
                        )
                    )
                )

                media = types.InputMediaDocument(
                    id=types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=b""
                    )
                )
            elif media.media.startswith("http"):
                media = types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, 9)

        if isinstance(media, InputMediaAnimation):
            if os.path.exists(media.media):
                media = self.send(
                    functions.messages.UploadMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "video/mp4",
                            thumb=None if media.thumb is None else self.save_file(media.thumb),
                            file=self.save_file(media.media),
                            attributes=[
                                types.DocumentAttributeVideo(
                                    supports_streaming=True,
                                    duration=media.duration,
                                    w=media.width,
                                    h=media.height
                                ),
                                types.DocumentAttributeFilename(
                                    file_name=os.path.basename(media.media)
                                ),
                                types.DocumentAttributeAnimated()
                            ]
                        )
                    )
                )

                media = types.InputMediaDocument(
                    id=types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=b""
                    )
                )
            elif media.media.startswith("http"):
                media = types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, 10)

        if isinstance(media, InputMediaDocument):
            if os.path.exists(media.media):
                media = self.send(
                    functions.messages.UploadMedia(
                        peer=self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type=self.guess_mime_type(media.media) or "application/zip",
                            thumb=None if media.thumb is None else self.save_file(media.thumb),
                            file=self.save_file(media.media),
                            attributes=[
                                types.DocumentAttributeFilename(
                                    file_name=os.path.basename(media.media)
                                )
                            ]
                        )
                    )
                )

                media = types.InputMediaDocument(
                    id=types.InputDocument(
                        id=media.document.id,
                        access_hash=media.document.access_hash,
                        file_reference=b""
                    )
                )
            elif media.media.startswith("http"):
                media = types.InputMediaDocumentExternal(
                    url=media.media
                )
            else:
                media = utils.get_input_media_from_file_id(media.media, 5)

        r = self.send(
            functions.messages.EditMessage(
                peer=self.resolve_peer(chat_id),
                id=message_id,
                reply_markup=reply_markup.write() if reply_markup else None,
                media=media,
                **style.parse(caption)
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateEditMessage, types.UpdateEditChannelMessage)):
                return pyrogram.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

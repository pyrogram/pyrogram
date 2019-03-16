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

import binascii
import os
import struct
from typing import Union

import pyrogram
from pyrogram.api import functions, types
from pyrogram.api.errors import FileIdInvalid
from pyrogram.client.ext import BaseClient, utils
from pyrogram.client.types import (
    InputMediaPhoto, InputMediaVideo, InputMediaAudio,
    InputMediaAnimation, InputMediaDocument
)
from pyrogram.client.types.input_media import InputMedia


class EditMessageMedia(BaseClient):
    async def edit_message_media(
        self,
        chat_id: Union[int, str],
        message_id: int,
        media: InputMedia,
        reply_markup: "pyrogram.InlineKeyboardMarkup" = None
    ) -> "pyrogram.Message":
        """Use this method to edit audio, document, photo, or video messages.

        If a message is a part of a message album, then it can be edited only to a photo or a video. Otherwise,
        message type can be changed arbitrarily. When inline message is edited, new file can't be uploaded.
        Use previously uploaded file via its file_id or specify a URL. On success, if the edited message was sent
        by the bot, the edited Message is returned, otherwise True is returned.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                Message identifier in the chat specified in chat_id.

            media (:obj:`InputMediaAnimation` | :obj:`InputMediaAudio` | :obj:`InputMediaDocument` | :obj:`InputMediaPhoto` | :obj:`InputMediaVideo`)
                One of the InputMedia objects describing an animation, audio, document, photo or video.

            reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
                An InlineKeyboardMarkup object.

        Returns:
            On success, the edited :obj:`Message <pyrogram.Message>` is returned.

        Raises:
            :class:`Error <pyrogram.Error>` in case of a Telegram RPC error.
        """
        style = self.html if media.parse_mode.lower() == "html" else self.markdown
        caption = media.caption

        if isinstance(media, InputMediaPhoto):
            if os.path.exists(media.media):
                media = await self.send(
                    functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedPhoto(
                            file=await self.save_file(media.media)
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
                try:
                    decoded = utils.decode(media.media)
                    fmt = "<iiqqqqi" if len(decoded) > 24 else "<iiqq"
                    unpacked = struct.unpack(fmt, decoded)
                except (AssertionError, binascii.Error, struct.error):
                    raise FileIdInvalid from None
                else:
                    if unpacked[0] != 2:
                        media_type = BaseClient.MEDIA_TYPE_ID.get(unpacked[0], None)

                        if media_type:
                            raise FileIdInvalid("The file_id belongs to a {}".format(media_type))
                        else:
                            raise FileIdInvalid("Unknown media type: {}".format(unpacked[0]))

                    media = types.InputMediaPhoto(
                        id=types.InputPhoto(
                            id=unpacked[2],
                            access_hash=unpacked[3],
                            file_reference=b""
                        )
                    )

        if isinstance(media, InputMediaVideo):
            if os.path.exists(media.media):
                media = await self.send(
                    functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type="video/mp4",
                            thumb=None if media.thumb is None else self.save_file(media.thumb),
                            file=await self.save_file(media.media),
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
                try:
                    decoded = utils.decode(media.media)
                    fmt = "<iiqqqqi" if len(decoded) > 24 else "<iiqq"
                    unpacked = struct.unpack(fmt, decoded)
                except (AssertionError, binascii.Error, struct.error):
                    raise FileIdInvalid from None
                else:
                    if unpacked[0] != 4:
                        media_type = BaseClient.MEDIA_TYPE_ID.get(unpacked[0], None)

                        if media_type:
                            raise FileIdInvalid("The file_id belongs to a {}".format(media_type))
                        else:
                            raise FileIdInvalid("Unknown media type: {}".format(unpacked[0]))

                    media = types.InputMediaDocument(
                        id=types.InputDocument(
                            id=unpacked[2],
                            access_hash=unpacked[3],
                            file_reference=b""
                        )
                    )

        if isinstance(media, InputMediaAudio):
            if os.path.exists(media.media):
                media = await self.send(
                    functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type="audio/mpeg",
                            thumb=None if media.thumb is None else self.save_file(media.thumb),
                            file=await self.save_file(media.media),
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
                try:
                    decoded = utils.decode(media.media)
                    fmt = "<iiqqqqi" if len(decoded) > 24 else "<iiqq"
                    unpacked = struct.unpack(fmt, decoded)
                except (AssertionError, binascii.Error, struct.error):
                    raise FileIdInvalid from None
                else:
                    if unpacked[0] != 9:
                        media_type = BaseClient.MEDIA_TYPE_ID.get(unpacked[0], None)

                        if media_type:
                            raise FileIdInvalid("The file_id belongs to a {}".format(media_type))
                        else:
                            raise FileIdInvalid("Unknown media type: {}".format(unpacked[0]))

                    media = types.InputMediaDocument(
                        id=types.InputDocument(
                            id=unpacked[2],
                            access_hash=unpacked[3],
                            file_reference=b""
                        )
                    )

        if isinstance(media, InputMediaAnimation):
            if os.path.exists(media.media):
                media = await self.send(
                    functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type="video/mp4",
                            thumb=None if media.thumb is None else self.save_file(media.thumb),
                            file=await self.save_file(media.media),
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
                try:
                    decoded = utils.decode(media.media)
                    fmt = "<iiqqqqi" if len(decoded) > 24 else "<iiqq"
                    unpacked = struct.unpack(fmt, decoded)
                except (AssertionError, binascii.Error, struct.error):
                    raise FileIdInvalid from None
                else:
                    if unpacked[0] != 10:
                        media_type = BaseClient.MEDIA_TYPE_ID.get(unpacked[0], None)

                        if media_type:
                            raise FileIdInvalid("The file_id belongs to a {}".format(media_type))
                        else:
                            raise FileIdInvalid("Unknown media type: {}".format(unpacked[0]))

                    media = types.InputMediaDocument(
                        id=types.InputDocument(
                            id=unpacked[2],
                            access_hash=unpacked[3],
                            file_reference=b""
                        )
                    )

        if isinstance(media, InputMediaDocument):
            if os.path.exists(media.media):
                media = await self.send(
                    functions.messages.UploadMedia(
                        peer=await self.resolve_peer(chat_id),
                        media=types.InputMediaUploadedDocument(
                            mime_type="application/zip",
                            thumb=None if media.thumb is None else self.save_file(media.thumb),
                            file=await self.save_file(media.media),
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
                try:
                    decoded = utils.decode(media.media)
                    fmt = "<iiqqqqi" if len(decoded) > 24 else "<iiqq"
                    unpacked = struct.unpack(fmt, decoded)
                except (AssertionError, binascii.Error, struct.error):
                    raise FileIdInvalid from None
                else:
                    if unpacked[0] not in (5, 10):
                        media_type = BaseClient.MEDIA_TYPE_ID.get(unpacked[0], None)

                        if media_type:
                            raise FileIdInvalid("The file_id belongs to a {}".format(media_type))
                        else:
                            raise FileIdInvalid("Unknown media type: {}".format(unpacked[0]))

                    media = types.InputMediaDocument(
                        id=types.InputDocument(
                            id=unpacked[2],
                            access_hash=unpacked[3],
                            file_reference=b""
                        )
                    )

        r = await self.send(
            functions.messages.EditMessage(
                peer=await self.resolve_peer(chat_id),
                id=message_id,
                reply_markup=reply_markup.write() if reply_markup else None,
                media=media,
                **style.parse(caption)
            )
        )

        for i in r.updates:
            if isinstance(i, (types.UpdateEditMessage, types.UpdateEditChannelMessage)):
                return await pyrogram.Message._parse(
                    self, i.message,
                    {i.id: i for i in r.users},
                    {i.id: i for i in r.chats}
                )

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

from typing import Optional, List

import pyrogram
from pyrogram import raw, types, utils, enums
from .inline_query_result import InlineQueryResult


class InlineQueryResultDocument(InlineQueryResult):
    """Link to a file.

    By default, this file will be sent by the user with an optional caption.
    Alternatively, you can use *input_message_content* to send a message with the specified content instead of the file.

    Parameters:
        document_url (``str``):
            A valid URL for the file.

        title (``str``):
            Title for the result.

        mime_type (``str``, *optional*):
            Mime type of the content of the file, either “application/pdf” or “application/zip”.
            Defaults to "application/zip".

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        caption (``str``, *optional*):
            Caption of the video to be sent, 0-1024 characters.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        description (``str``, *optional*):
            Short description of the result.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.

        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent instead of the file.

        thumb_url (``str``, *optional*):
            Url of the thumbnail for the result.

        thumb_width (``int``, *optional*):
            Thumbnail width.

        thumb_height (``int``, *optional*):
            Thumbnail height.
    """

    def __init__(
        self,
        document_url: str,
        title: str,
        mime_type: str = "application/zip",
        id: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        description: str = "",
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None,
        thumb_url: str = None,
        thumb_width: int = 0,
        thumb_height: int = 0
    ):
        super().__init__("file", id, input_message_content, reply_markup)

        self.document_url = document_url
        self.title = title
        self.mime_type = mime_type
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    async def write(self, client: "pyrogram.Client"):
        document = raw.types.InputWebDocument(
            url=self.document_url,
            size=0,
            mime_type=self.mime_type,
            attributes=[]
        )

        thumb = raw.types.InputWebDocument(
            url=self.thumb_url,
            size=0,
            mime_type="image/jpeg",
            attributes=[
                raw.types.DocumentAttributeImageSize(
                    w=self.thumb_width,
                    h=self.thumb_height
                )
            ]
        ) if self.thumb_url else None

        message, entities = (await utils.parse_text_entities(
            client, self.caption, self.parse_mode, self.caption_entities
        )).values()

        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=thumb,
            content=document,
            send_message=(
                await self.input_message_content.write(client, self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=await self.reply_markup.write(client) if self.reply_markup else None,
                    message=message,
                    entities=entities
                )
            )
        )

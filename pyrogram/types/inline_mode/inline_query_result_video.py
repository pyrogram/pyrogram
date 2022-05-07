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


class InlineQueryResultVideo(InlineQueryResult):
    """Link to a page containing an embedded video player or a video file.

    By default, this video file will be sent by the user with an optional caption.
    Alternatively, you can use *input_message_content* to send a message with the specified content instead of the
    video.

    Parameters:
        video_url (``str``):
            A valid URL for the embedded video player or video file.

        thumb_url (``str``):
            URL of the thumbnail (jpeg only) for the video.

        title (``str``):
            Title for the result.

        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.

        mime_type (``str``):
            Mime type of the content of video url, "text/html" or "video/mp4".
            Defaults to "video/mp4".

        video_width (``int``):
            Video width.

        video_height (``int``):
            Video height.

        video_duration (``int``):
            Video duration in seconds.

        description (``str``, *optional*):
            Short description of the result.

        caption (``str``, *optional*):
            Caption of the video to be sent, 0-1024 characters.

        parse_mode (:obj:`~pyrogram.enums.ParseMode`, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.

        caption_entities (List of :obj:`~pyrogram.types.MessageEntity`):
            List of special entities that appear in the caption, which can be specified instead of *parse_mode*.

        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message

        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent instead of the video. This field is required if InlineQueryResultVideo is
            used to send an HTML-page as a result (e.g., a YouTube video).
    """

    def __init__(
        self,
        video_url: str,
        thumb_url: str,
        title: str,
        id: str = None,
        mime_type: str = "video/mp4",
        video_width: int = 0,
        video_height: int = 0,
        video_duration: int = 0,
        description: str = None,
        caption: str = "",
        parse_mode: Optional["enums.ParseMode"] = None,
        caption_entities: List["types.MessageEntity"] = None,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("video", id, input_message_content, reply_markup)

        self.video_url = video_url
        self.thumb_url = thumb_url
        self.title = title
        self.video_width = video_width
        self.video_height = video_height
        self.video_duration = video_duration
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.caption_entities = caption_entities
        self.mime_type = mime_type

    async def write(self, client: "pyrogram.Client"):
        video = raw.types.InputWebDocument(
            url=self.video_url,
            size=0,
            mime_type=self.mime_type,
            attributes=[raw.types.DocumentAttributeVideo(
                duration=self.video_duration,
                w=self.video_width,
                h=self.video_height
            )]
        )

        thumb = raw.types.InputWebDocument(
            url=self.thumb_url,
            size=0,
            mime_type="image/jpeg",
            attributes=[]
        )

        message, entities = (await utils.parse_text_entities(
            client, self.caption, self.parse_mode, self.caption_entities
        )).values()

        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=thumb,
            content=video,
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

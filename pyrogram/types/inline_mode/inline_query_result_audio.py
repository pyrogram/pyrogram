#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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

from typing import Optional

from pyrogram import raw
from pyrogram import types
from pyrogram.parser import Parser
from .inline_query_result import InlineQueryResult


class InlineQueryResultAudio(InlineQueryResult):
    """Link to an audio.
    By default, this audio will be sent by the user with optional caption.
    Alternatively, you can use *input_message_content* to send a message 
    with the specified content instead of the audio.
    Parameters:
        audio_url (``str``):
            A valid URL for the embedded audio player or audio file.
        thumb_url (``str``):
            URL of the thumbnail (jpeg only) for the audio.
        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.
        title (``str``, *optional*):
            Title for the result.
        mime_type (``str``, *optional*):
            Mime type of the content of audio url, “text/html” or “audio/mp3”.
        description (``str``, *optional*):
            Short description of the result.
        caption (``str``, *optional*):
            Caption of the audio to be sent, 0-1024 characters.
        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.
        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            An InlineKeyboardMarkup object.
        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent instead of the audio. This field is required if InlineQueryResultAudio is
            used to send an HTML-page as a result.
    """

    def __init__(
        self,
        audio_url: str,
        thumb_url: str,
        id: str = None,
        title: str = None,
        mime_type: str = None,
        description: str = None,
        caption: str = "",
        parse_mode: Optional[str] = object,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("audio", id, input_message_content, reply_markup)

        self.audio_url = audio_url

        self.thumb_url = thumb_url
        self.title = title

        if mime_type != "text/html" and mime_type != "audio/mp3":
            raise ValueError("Invalid mime type")

        self.mime_type = mime_type
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup

        if mime_type == "text/html" and input_message_content is None:
            raise ValueError("input_message_content is required for audio with `text/html` mime type")

        self.input_message_content = input_message_content

    async def write(self):
        audio = raw.types.InputWebDocument(
            url=self.audio_url,
            size=0,
            mime_type=self.mime_type,
            attributes=[]
        )

        thumb = raw.types.InputWebDocument(
            url=self.thumb_url,
            size=0,
            mime_type="image/jpeg",
            attributes=[]
        )

        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=thumb,
            content=audio,
            send_message=(
                await self.input_message_content.write(self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=self.reply_markup.write() if self.reply_markup else None,
                    **await(Parser(None)).parse(self.caption, self.parse_mode)
                )
            )
        )

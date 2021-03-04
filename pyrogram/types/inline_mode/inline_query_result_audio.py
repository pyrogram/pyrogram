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

from typing import Union

from pyrogram import raw
from pyrogram import types
from pyrogram.parser import Parser
from pyrogram.types import InlineQueryResult


class InlineQueryResultAudio(InlineQueryResult):
    """Link to an audio file.
    By default, this audio file will be sent by the user with optional caption.
    Alternatively, you can use *input_message_content* to send a message with the specified content instead of the
    audio.
    Parameters:
        audio_url (``str``):
            A valid URL for the audio file.
        title (``str``):
            Title for the result.
        duration (``int``, *optional*):
            Duration of the audio in second.
        voice (``bool``, *optional*):
            Whether this file should be sent as voice message (default=False).
        performer (``str``, *optional*):
            Audio artist.
        thumb_url (``str``, *optional*):
            URL of the static thumbnail for the result (jpeg or gif)
            Defaults to the value passed in *animation_url*.
        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.
        description (``str``, *optional*):
            Short description of the result.
        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters.
        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.
        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            An InlineKeyboardMarkup object.
        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent instead of the photo.
    """

    def __init__(
            self,
            audio_url: str,
            title: str,
            duration: int = 0,
            voice: bool = False,
            performer: str = "",
            thumb_url: str = None,
            id: str = None,
            description: str = None,
            caption: str = "",
            parse_mode: Union[str, None] = object,
            reply_markup: "types.InlineKeyboardMarkup" = None,
            input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("audio", id, input_message_content, reply_markup)

        self.audio_url = audio_url
        self.thumb_url = thumb_url
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content
        self.duration = duration
        self.voice = voice
        self.performer = performer

    async def write(self):
        audio = raw.types.InputWebDocument(
            url=self.audio_url,
            size=0,
            mime_type="audio/ogg",
            attributes=[raw.types.DocumentAttributeAudio(
                duration=self.duration,
                voice=self.voice,
                title=self.title,
                performer=self.performer,
                # waveform=idk wtf is that...
            )],
        )

        return raw.types.InputBotInlineResult(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            thumb=raw.types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[]
            ) if self.thumb_url else None,
            content=audio,
            send_message=(
                self.input_message_content.write(self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=self.reply_markup.write() if self.reply_markup else None,
                    **await(Parser(None)).parse(self.caption, self.parse_mode)
                )
            )
        )

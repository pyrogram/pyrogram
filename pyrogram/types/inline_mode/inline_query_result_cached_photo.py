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
from pyrogram import utils
from pyrogram import types
from pyrogram.parser import Parser
from pyrogram.file_id import FileType
from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedPhoto(InlineQueryResult):
    """Link to a photo stored on the Telegram servers.
    
    By default, this photo will be sent by the user with an optional caption. 
    Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.
    
    Parameters:
        file_id (``str``):
            Pass a file_id as string to send a media that exists on the Telegram servers.
            
        id (``str``, *optional*):
            Unique identifier for this result, 1-64 bytes.
            Defaults to a randomly generated UUID4.
            
        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-1024 characters.
        
        parse_mode (``str``, *optional*):
            By default, texts are parsed using both Markdown and HTML styles.
            You can combine both syntaxes together.
            Pass "markdown" or "md" to enable Markdown-style parsing only.
            Pass "html" to enable HTML-style parsing only.
            Pass None to completely disable style parsing.
            
        reply_markup (:obj:`~pyrogram.types.InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.
            
        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent.
    """

    def __init__(
        self,
        file_id: str,
        id: str = None,
        caption: str = "",
        parse_mode: Union[str, None] = object,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("photo", id, input_message_content, reply_markup)

        self.file_id = file_id
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    async def write(self):
        photo = utils.get_input_file_from_file_id(self.file_id, FileType.PHOTO)

        return raw.types.InputBotInlineResultPhoto(
            id=self.id,
            type=self.type,
            photo=photo,
            send_message=(
                await self.input_message_content.write(self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=self.reply_markup.write() if self.reply_markup else None,
                    **await (Parser(None)).parse(self.caption, self.parse_mode)
                )
            )
        )
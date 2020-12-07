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
from .inline_query_result import InlineQueryResult


class InlineQueryResultCachedDocument(InlineQueryResult):
    """Link to a file stored on the Telegram servers.

    By default, this file will be sent by the user with an optional caption. 
    Alternatively, you can use input_message_content to send a message with the specified content instead of the file.

    Parameters:
        title (``str``):
            Title for the result.
        
        file_id (``str``):
            Pass a file_id as string to send a media that exists on the Telegram servers.

        file_ref (``str``, *optional*):
            A valid file reference obtained by a recently fetched media message.
            To be used in combination with a file id in case a file reference is needed.

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
            Inline keyboard attached to the message.

        input_message_content (:obj:`~pyrogram.types.InputMessageContent`):
            Content of the message to be sent.
    """

    def __init__(
        self,
        title: str,
        file_id: str,
        file_ref: str = None,
        id: str = None,
        description: str = None,
        caption: str = "",
        parse_mode: Union[str, None] = object,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("file", id, input_message_content, reply_markup)

        self.file_id = file_id
        self.file_ref = file_ref
        self.title = title
        self.description = description
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    async def write(self):
        document = utils.get_input_file_from_file_id(self.file_id, self.file_ref)

        return raw.types.InputBotInlineResultDocument(
            id=self.id,
            type=self.type,
            title=self.title,
            description=self.description,
            document=document,
            send_message=(
                await self.input_message_content.write(self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=self.reply_markup.write() if self.reply_markup else None,
                    **await(Parser(None)).parse(self.caption, self.parse_mode)
                )
            )
        ) 
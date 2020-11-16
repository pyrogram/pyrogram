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


class InlineQueryResultCachedPhoto(InlineQueryResult):

    # TODO: Need to add documentation 

    def __init__(
        self,
        file_id: str,
        file_ref: str = None,
        id: str = None,
        caption: str = "",
        parse_mode: Union[str, None] = object,
        reply_markup: "types.InlineKeyboardMarkup" = None,
        input_message_content: "types.InputMessageContent" = None
    ):
        super().__init__("photo", id, input_message_content, reply_markup)

        self.file_id = file_id
        self.file_ref = file_ref
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

    async def write(self):
        photo = utils.get_input_file_from_file_id(self.file_id, self.file_ref, 2)

        return raw.types.InputBotInlineResultPhoto(
            id=self.id,
            type=self.type,
            photo=photo,
            send_message=(
                await self.input_message_content.write(self.reply_markup)
                if self.input_message_content
                else raw.types.InputBotInlineMessageMediaAuto(
                    reply_markup=self.reply_markup.write() if self.reply_markup else None,
                    **await(Parser(None)).parse(self.caption, self.parse_mode)
                )
            )
        )  
# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

from typing import Any

from pyrogram.api import types
from .inline_query_result import InlineQueryResult


class InlineQueryResultArticle(InlineQueryResult):
    """Represents a link to an article or web page.

    TODO: Hide url?

    Parameters:
        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        title (``str``):
            Title for the result.

        input_message_content (:obj:`InputMessageContent <pyrogram.InputMessageContent>`):
            Content of the message to be sent.

        reply_markup (:obj:`InlineKeyboardMarkup <pyrogram.InlineKeyboardMarkup>`, *optional*):
            Inline keyboard attached to the message.

        url (``str``, *optional*):
            URL of the result.

        description (``str``, *optional*):
            Short description of the result.

        thumb_url (``str``, *optional*):
            Url of the thumbnail for the result.

        thumb_width (``int``, *optional*):
            Thumbnail width.

        thumb_height (``int``, *optional*):
            Thumbnail height.
    """

    __slots__ = [
        "title", "input_message_content", "reply_markup", "url", "description", "thumb_url", "thumb_width",
        "thumb_height"
    ]

    def __init__(
        self,
        id: Any,
        title: str,
        input_message_content,
        reply_markup=None,
        url: str = None,
        description: str = None,
        thumb_url: str = None,
        thumb_width: int = 0,
        thumb_height: int = 0
    ):
        super().__init__("article", id)

        self.title = title
        self.input_message_content = input_message_content
        self.reply_markup = reply_markup
        self.url = url
        self.description = description
        self.thumb_url = thumb_url
        self.thumb_width = thumb_width
        self.thumb_height = thumb_height

    def write(self):
        return types.InputBotInlineResult(
            id=str(self.id),
            type=self.type,
            send_message=self.input_message_content.write(self.reply_markup),
            title=self.title,
            description=self.description,
            url=self.url,
            thumb=types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[
                    types.DocumentAttributeImageSize(
                        w=self.thumb_width,
                        h=self.thumb_height
                    )
                ]
            ) if self.thumb_url else None
        )

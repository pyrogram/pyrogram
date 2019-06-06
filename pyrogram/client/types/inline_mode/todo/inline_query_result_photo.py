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

from pyrogram.api import types
from pyrogram.client.style import HTML, Markdown
from pyrogram.client.types.object import Object


class InlineQueryResultPhoto(Object):
    """Represents a link to a photo. By default, this photo will be sent by the user with optional caption.
    Alternatively, you can use input_message_content to send a message with the specified content instead of the photo.

    Parameters:
        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        photo_url (``str``):
            A valid URL of the photo. Photo must be in jpeg format. Photo size must not exceed 5MB.

        thumb_url (``str``):
            URL of the thumbnail for the photo.

        photo_width (``int``, *optional*):
            Width of the photo.

        photo_height (``int``, *optional*):
            Height of the photo.

        title (``str``, *optional*):
            Title for the result.

        description (``str``, *optional*):
            Short description of the result.

        caption (``str``, *optional*):
            Caption of the photo to be sent, 0-200 characters.

        parse_mode (``str``, *optional*):
            Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in
            the media caption.

        reply_markup (:obj:`InlineKeyboardMarkup`, *optional*):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent`, *optional*):
            Content of the message to be sent instead of the photo.

    """

    def __init__(
        self,
        id: str,
        photo_url: str,
        thumb_url: str,
        photo_width: int = 0,
        photo_height: int = 0,
        title: str = None,
        description: str = None,
        caption: str = "",
        parse_mode: str = "",
        reply_markup=None,
        input_message_content=None
    ):
        self.id = id  # string
        self.photo_url = photo_url  # string
        self.thumb_url = thumb_url  # string
        self.photo_width = photo_width  # flags.0?int
        self.photo_height = photo_height  # flags.1?int
        self.title = title  # flags.2?string
        self.description = description  # flags.3?string
        self.caption = caption  # flags.4?string
        self.parse_mode = parse_mode  # flags.5?string
        self.reply_markup = reply_markup  # flags.6?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.7?InputMessageContent

        self.style = HTML() if parse_mode.lower() == "html" else Markdown()

    def write(self):
        return types.InputBotInlineResult(
            id=self.id,
            type="photo",
            send_message=types.InputBotInlineMessageMediaAuto(
                reply_markup=self.reply_markup.write() if self.reply_markup else None,
                **self.style.parse(self.caption)
            ),
            title=self.title,
            description=self.description,
            url=self.photo_url,
            thumb=types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[
                    types.DocumentAttributeImageSize(
                        w=0,
                        h=0
                    )
                ]
            ),
            content=types.InputWebDocument(
                url=self.thumb_url,
                size=0,
                mime_type="image/jpeg",
                attributes=[
                    types.DocumentAttributeImageSize(
                        w=self.photo_width,
                        h=self.photo_height
                    )
                ]
            )
        )

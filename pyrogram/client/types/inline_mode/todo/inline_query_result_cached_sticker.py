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

from pyrogram.client.types.pyrogram_type import PyrogramType


class InlineQueryResultCachedSticker(PyrogramType):
    """Represents a link to a sticker stored on the Telegram servers. By default, this sticker will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the sticker.

    Attributes:
        ID: ``0xb0700014``

    Parameters:
        type (``str``):
            Type of the result, must be sticker.

        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        sticker_file_id (``str``):
            A valid file identifier of the sticker.

        reply_markup (:obj:`InlineKeyboardMarkup`, optional):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent`, optional):
            Content of the message to be sent instead of the sticker.

    """
    ID = 0xb0700014

    def __init__(self, type: str, id: str, sticker_file_id: str, reply_markup=None, input_message_content=None):
        self.type = type  # string
        self.id = id  # string
        self.sticker_file_id = sticker_file_id  # string
        self.reply_markup = reply_markup  # flags.0?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.1?InputMessageContent

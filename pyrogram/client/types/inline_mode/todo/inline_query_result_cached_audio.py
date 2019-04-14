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

import binascii
import struct

from pyrogram.api import types
from pyrogram.errors import FileIdInvalid
from pyrogram.client.ext import utils, BaseClient
from pyrogram.client.style import HTML, Markdown
from pyrogram.client.types.pyrogram_type import PyrogramType


class InlineQueryResultCachedAudio(PyrogramType):
    """Represents a link to an audio file stored on the Telegram servers.
    By default, this audio file will be sent by the user. Alternatively, you can use *input_message_content* to send a
    message with the specified content instead of the audio.

    Args:
        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        audio_file_id (``str``):
            A valid file identifier for the audio file.

        caption (``str``, *optional*):
            Caption, 0-200 characters.

        parse_mode (``str``, *optional*):
            Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in
            the media caption.

        reply_markup (:obj:`InlineKeyboardMarkup <pyrogram.types.InlineKeyboardMarkup>`, *optional*):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent <pyrogram.types.InputMessageContent>`, *optional*):
            Content of the message to be sent instead of the audio.

    """

    def __init__(
        self,
        id: str,
        audio_file_id: str,
        caption: str = "",
        parse_mode: str = "",
        reply_markup=None,
        input_message_content=None
    ):
        self.id = id
        self.audio_file_id = audio_file_id
        self.caption = caption
        self.parse_mode = parse_mode
        self.reply_markup = reply_markup
        self.input_message_content = input_message_content

        self.style = HTML() if parse_mode.lower() == "html" else Markdown()

    def write(self):
        try:
            decoded = utils.decode(self.audio_file_id)
            fmt = "<iiqqqqi" if len(decoded) > 24 else "<iiqq"
            unpacked = struct.unpack(fmt, decoded)
        except (AssertionError, binascii.Error, struct.error):
            raise FileIdInvalid from None
        else:
            if unpacked[0] != 9:
                media_type = BaseClient.MEDIA_TYPE_ID.get(unpacked[0], None)

                if media_type:
                    raise FileIdInvalid("The file_id belongs to a {}".format(media_type))
                else:
                    raise FileIdInvalid("Unknown media type: {}".format(unpacked[0]))

        audio = types.InputDocument(
            id=unpacked[2],
            access_hash=unpacked[3]
        )

        return types.InputBotInlineResultDocument(
            id=self.id,
            type="audio",
            document=audio,
            send_message=types.InputBotInlineMessageMediaAuto(
                reply_markup=self.reply_markup.write() if self.reply_markup else None,
                **self.style.parse(self.caption)
            )
        )

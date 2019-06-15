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

from pyrogram.client.types.object import Object


class InlineQueryResultAudio(Object):
    """Represents a link to an mp3 audio file. By default, this audio file will be sent by the user. Alternatively, you can use input_message_content to send a message with the specified content instead of the audio.

    Attributes:
        ID: ``0xb0700004``

    Parameters:
        type (``str``):
            Type of the result, must be audio.

        id (``str``):
            Unique identifier for this result, 1-64 bytes.

        audio_url (``str``):
            A valid URL for the audio file.

        title (``str``):
            Title.

        caption (``str``, optional):
            Caption, 0-200 characters.

        parse_mode (``str``, optional):
            Send Markdown or HTML, if you want Telegram apps to show bold, italic, fixed-width text or inline URLs in the media caption.

        performer (``str``, optional):
            Performer.

        audio_duration (``int`` ``32-bit``, optional):
            Audio duration in seconds.

        reply_markup (:obj:`InlineKeyboardMarkup`, optional):
            Inline keyboard attached to the message.

        input_message_content (:obj:`InputMessageContent`, optional):
            Content of the message to be sent instead of the audio.

    """

    def __init__(self, type: str, id: str, audio_url: str, title: str, caption: str = None, parse_mode: str = None,
                 performer: str = None, audio_duration: int = None, reply_markup=None, input_message_content=None):
        self.type = type  # string
        self.id = id  # string
        self.audio_url = audio_url  # string
        self.title = title  # string
        self.caption = caption  # flags.0?string
        self.parse_mode = parse_mode  # flags.1?string
        self.performer = performer  # flags.2?string
        self.audio_duration = audio_duration  # flags.3?int
        self.reply_markup = reply_markup  # flags.4?InlineKeyboardMarkup
        self.input_message_content = input_message_content  # flags.5?InputMessageContent

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

from pyrogram.api.core import Object


class CallbackQuery(Object):
    """This object represents an incoming callback query from a callback button in an inline keyboard.
    If the button that originated the query was attached to a message sent by the bot, the field message
    will be present. If the button was attached to a message sent via the bot (in inline mode),
    the field inline_message_id will be present. Exactly one of the fields data or game_short_name will be present.

    Args:
        id (``str``):
            Unique identifier for this query.

        from_user (:obj:`User <pyrogram.User>`):
            Sender.

        chat_instance (``str``, *optional*):
            Message with the callback button that originated the query. Note that message content and message date will
            not be available if the message is too old.

        message (:obj:`Message <pyrogram.Message>`, *optional*):
            Identifier of the message sent via the bot in inline mode, that originated the query.

        inline_message_id (``str``):
            Global identifier, uniquely corresponding to the chat to which the message with the callback button was
            sent. Useful for high scores in games.

        data (``str``, *optional*):
            Data associated with the callback button. Be aware that a bad client can send arbitrary data in this field.

        game_short_name (``str``, *optional*):
            Short name of a Game to be returned, serves as the unique identifier for the game.

    """
    ID = 0xb0700024

    def __init__(
            self,
            id: str,
            from_user,
            chat_instance: str,
            message=None,
            inline_message_id: str = None,
            data: str = None,
            game_short_name: str = None
    ):
        self.id = id  # string
        self.from_user = from_user  # User
        self.message = message  # flags.0?Message
        self.inline_message_id = inline_message_id  # flags.1?string
        self.chat_instance = chat_instance  # string
        self.data = data  # flags.2?string
        self.game_short_name = game_short_name  # flags.3?string

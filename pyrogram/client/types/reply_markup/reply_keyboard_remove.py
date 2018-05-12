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
from pyrogram.api.types import ReplyKeyboardHide


class ReplyKeyboardRemove(Object):
    """Upon receiving a message with this object, Telegram clients will remove the current custom keyboard and
    display the default letter-keyboard. By default, custom keyboards are displayed until a new keyboard is sent
    by a bot. An exception is made for one-time keyboards that are hidden immediately after the user presses a
    button (see ReplyKeyboardMarkup).

    Args:
        selective (``bool``, *optional*):
            Use this parameter if you want to remove the keyboard for specific users only. Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
            Example: A user votes in a poll, bot returns confirmation message in reply to the vote and removes the
            keyboard for that user, while still showing the keyboard with poll options to users who haven't voted yet.
    """

    ID = 0xb0700002

    def __init__(self, selective: bool = None):
        self.selective = selective

    @staticmethod
    def read(o, *args):
        return ReplyKeyboardRemove(
            selective=o.selective
        )

    def write(self):
        return ReplyKeyboardHide(
            selective=self.selective or None
        )

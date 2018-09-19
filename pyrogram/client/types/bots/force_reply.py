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
from pyrogram.api.types import ReplyKeyboardForceReply


class ForceReply(Object):
    """Upon receiving a message with this object, Telegram clients will display a reply interface to the user
    (act as if the user has selected the bot's message and tapped 'Reply').
    This can be extremely useful if you want to create user-friendly step-by-step interfaces without having to
    sacrifice privacy mode.

    Args:
        selective (``bool``, *optional*):
            Use this parameter if you want to force reply from specific users only. Targets:
            1) users that are @mentioned in the text of the Message object;
            2) if the bot's message is a reply (has reply_to_message_id), sender of the original message.
    """

    ID = 0xb0700018

    def __init__(self, selective: bool = None):
        self.selective = selective

    @staticmethod
    def read(o, *args):
        return ForceReply(
            selective=o.selective
        )

    def write(self):
        return ReplyKeyboardForceReply(
            single_use=True,
            selective=self.selective or None
        )

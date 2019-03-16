# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
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

from typing import List

from pyrogram.api.types import ReplyInlineMarkup, KeyboardButtonRow
from . import InlineKeyboardButton
from ..pyrogram_type import PyrogramType


class InlineKeyboardMarkup(PyrogramType):
    """This object represents an inline keyboard that appears right next to the message it belongs to.

    Args:
        inline_keyboard (List of List of :obj:`InlineKeyboardButton <pyrogram.InlineKeyboardButton>`):
            List of button rows, each represented by a List of InlineKeyboardButton objects.
    """

    __slots__ = ["inline_keyboard"]

    def __init__(
            self,
            inline_keyboard: List[List[InlineKeyboardButton]]
    ):
        super().__init__(None)

        self.inline_keyboard = inline_keyboard

    @staticmethod
    def read(o):
        inline_keyboard = []

        for i in o.rows:
            row = []

            for j in i.buttons:
                row.append(InlineKeyboardButton.read(j))

            inline_keyboard.append(row)

        return InlineKeyboardMarkup(
            inline_keyboard=inline_keyboard
        )

    def write(self):
        return ReplyInlineMarkup(
            [KeyboardButtonRow(
                [j.write() for j in i]
            ) for i in self.inline_keyboard]
        )

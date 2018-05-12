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

from pyrogram.api.types import KeyboardButton as RawKeyboardButton
from pyrogram.api.types import KeyboardButtonRequestPhone, KeyboardButtonRequestGeoLocation


class KeyboardButton(Object):
    """This object represents one button of the reply keyboard.
    For simple text buttons String can be used instead of this object to specify text of the button.
    Optional fields are mutually exclusive.

    Args:
        text (``str``):
            Text of the button. If none of the optional fields are used, it will be sent as a message when
            the button is pressed.

        request_contact (``bool``, *optional*):
            If True, the user's phone number will be sent as a contact when the button is pressed.
            Available in private chats only.

        request_location (``bool``, *optional*):
            If True, the user's current location will be sent when the button is pressed.
            Available in private chats only.
    """

    ID = 0xb0700021

    def __init__(self, text: str, request_contact: bool = None, request_location: bool = None):
        self.text = text
        self.request_contact = request_contact
        self.request_location = request_location

    @staticmethod
    def read(b, *args):
        if isinstance(b, RawKeyboardButton):
            return b.text

        if isinstance(b, KeyboardButtonRequestPhone):
            return KeyboardButton(
                text=b.text,
                request_contact=True
            )

        if isinstance(b, KeyboardButtonRequestGeoLocation):
            return KeyboardButton(
                text=b.text,
                request_location=True
            )

    def write(self):
        # TODO: Enforce optional args mutual exclusiveness

        if self.request_contact:
            return KeyboardButtonRequestPhone(self.text)
        elif self.request_location:
            return KeyboardButtonRequestGeoLocation(self.text)
        else:
            return RawKeyboardButton(self.text)

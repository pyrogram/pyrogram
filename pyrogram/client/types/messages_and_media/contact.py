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
from ..pyrogram_type import PyrogramType


class Contact(PyrogramType):
    """This object represents a phone contact.

    Args:
        phone_number (``str``):
            Contact's phone number.

        first_name (``str``):
            Contact's first name.

        last_name (``str``, *optional*):
            Contact's last name.

        user_id (``int``, *optional*):
            Contact's user identifier in Telegram.

        vcard (``str``, *optional*):
            Additional data about the contact in the form of a vCard.
    """

    def __init__(self, phone_number: str, first_name: str, *,
                 last_name: str = None, user_id: int = None, vcard: str = None,
                 client=None, raw=None):
        self.phone_number = phone_number
        self.first_name = first_name
        self.last_name = last_name
        self.user_id = user_id
        self.vcard = vcard

        self._client = client
        self._raw = raw

    @staticmethod
    def parse(client, contact: types.MessageMediaContact) -> "Contact":
        return Contact(
            phone_number=contact.phone_number,
            first_name=contact.first_name,
            last_name=contact.last_name or None,
            vcard=contact.vcard or None,
            user_id=contact.user_id or None,
            client=client,
            raw=contact
        )

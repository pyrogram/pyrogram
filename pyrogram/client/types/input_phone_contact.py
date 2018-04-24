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

from pyrogram.api.types import InputPhoneContact as RawInputPhoneContact
from pyrogram.session.internals import MsgId


class InputPhoneContact:
    """This object represents a Phone Contact to be added in your Telegram address book.
    It is intended to be used with :meth:`add_contacts() <pyrogram.Client.add_contacts>`

    Args:
        phone (``str``):
            Contact's phone number

        first_name (``str``):
            Contact's first name

        last_name (``str``, *optional*):
            Contact's last name
    """

    def __init__(self, phone: str, first_name: str, last_name: str = ""):
        pass

    def __new__(cls, phone: str, first_name: str, last_name: str = ""):
        return RawInputPhoneContact(
            client_id=MsgId(),
            phone="+" + phone.strip("+"),
            first_name=first_name,
            last_name=last_name
        )

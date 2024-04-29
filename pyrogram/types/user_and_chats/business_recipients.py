#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import List

from pyrogram import types, raw
from ..object import Object


class BusinessRecipients(Object):
    """Business recipients.

    Parameters:
        existing_chats (``bool``, *optional*):
            True, if the message should be sent to existing chats.

        new_chats (``bool``, *optional*):
            True, if the message should be sent to new chats.

        contacts (``bool``, *optional*):
            True, if the message should be sent to contacts.

        non_contacts (``bool``, *optional*):
            True, if the message should be sent to non-contacts.

        exclude_selected (``bool``, *optional*):
            True, if the message should be sent to non-selected contacts.

        users (List of :obj:`~pyrogram.types.User`, *optional*):
            Recipients of the message.
    """

    def __init__(
        self,
        *,
        existing_chats: bool = None,
        new_chats: bool = None,
        contacts: bool = None,
        non_contacts: bool = None,
        exclude_selected: bool = None,
        users: List[int] = None
    ):
        self.existing_chats = existing_chats
        self.new_chats = new_chats
        self.contacts = contacts
        self.non_contacts = non_contacts
        self.exclude_selected = exclude_selected
        self.users = users

    @staticmethod
    def _parse(
        client,
        recipients: "raw.types.BusinessRecipients",
        users: dict = None
    ) -> "BusinessRecipients":
        return BusinessRecipients(
            existing_chats=getattr(recipients, "existing_chats", None),
            new_chats=getattr(recipients, "new_chats", None),
            contacts=getattr(recipients, "contacts", None),
            non_contacts=getattr(recipients, "non_contacts", None),
            exclude_selected=getattr(recipients, "exclude_selected", None),
            users=types.List(types.User._parse(client, users[i]) for i in recipients.users) or None if getattr(recipients, "users", None) else None
        )

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

from pyrogram.api import functions, types
from pyrogram.api.errors import PeerIdInvalid
from ...ext import BaseClient


class DeleteContacts(BaseClient):
    def delete_contacts(self, ids: list):
        """Use this method to delete contacts from your Telegram address book

        Args:
            ids (``list``):
                A list of unique identifiers for the target users.
                Can be an ID (int), a username (string) or phone number (string).

        Returns:
            True on success.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        contacts = []

        for i in ids:
            try:
                input_user = self.resolve_peer(i)
            except PeerIdInvalid:
                continue
            else:
                if isinstance(input_user, types.InputPeerUser):
                    contacts.append(input_user)

        return self.send(
            functions.contacts.DeleteContacts(
                id=contacts
            )
        )

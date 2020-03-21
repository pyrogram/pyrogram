#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

import logging
import time
from typing import List

import pyrogram
from pyrogram.api import functions
from pyrogram.errors import FloodWait
from ...ext import BaseClient

log = logging.getLogger(__name__)


class GetContacts(BaseClient):
    def get_contacts(self) -> List["pyrogram.User"]:
        """Get contacts from your Telegram address book.

        Returns:
            List of :obj:`User`: On success, a list of users is returned.

        Example:
            .. code-block:: python

                contacts = app.get_contacts()
                print(contacts)
        """
        while True:
            try:
                contacts = self.send(functions.contacts.GetContacts(hash=0))
            except FloodWait as e:
                log.warning("get_contacts flood: waiting {} seconds".format(e.x))
                time.sleep(e.x)
            else:
                return pyrogram.List(pyrogram.User._parse(self, user) for user in contacts.users)

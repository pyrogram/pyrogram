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

import time

from pyrogram import Client
from pyrogram.api.errors import FloodWait

app = Client("my_account")

target = "pyrogramchat"  # Target channel/supergroup
members = []  # List that will contain all the members of the target chat
offset = 0  # Offset starts at 0
limit = 200  # Amount of users to retrieve for each API call (max 200)

with app:
    while True:
        try:
            chunk = app.get_chat_members(target, offset)
        except FloodWait as e:  # Very large chats could trigger FloodWait
            time.sleep(e.x)  # When it happens, wait X seconds and try again
            continue

        if not chunk.chat_members:
            break  # No more members left

        members.extend(chunk.chat_members)
        offset += len(chunk.chat_members)

# Now the "members" list contains all the members of the target chat

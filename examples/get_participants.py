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
from pyrogram.api import functions, types
from pyrogram.api.errors import FloodWait

"""This simple GetParticipants method usage shows you how to get the first 10.000 users of a chat.

Refer to get_participants2.py for more than 10.000 users.
"""

app = Client("my_account")
target = "pyrogramchat"  # Target channel/supergroup
users = []  # List that will contain all the users of the target chat
limit = 200  # Amount of users to retrieve for each API call
offset = 0  # Offset starts at 0

app.start()

while True:
    try:
        participants = app.send(
            functions.channels.GetParticipants(
                channel=app.resolve_peer(target),
                filter=types.ChannelParticipantsSearch(""),  # Filter by empty string (search for all)
                offset=offset,
                limit=limit,
                hash=0
            )
        )
    except FloodWait as e:
        # Very large channels will trigger FloodWait.
        # When happens, wait X seconds before continuing
        time.sleep(e.x)
        continue

    if not participants.participants:
        break  # No more participants left

    users.extend(participants.users)
    offset += limit

app.stop()

# Now the "users" list contains all the members of the target chat

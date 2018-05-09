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
from string import ascii_lowercase

from pyrogram import Client
from pyrogram.api import functions, types
from pyrogram.api.errors import FloodWait

"""This is an improved version of get_participants.py

Since Telegram will return at most 10.000 users for a single query, this script
repeats the search using numbers ("0" to "9") and all the available ascii letters ("a" to "z").

This can be further improved by also searching for non-ascii characters (e.g.: Japanese script),
as some user names may not contain ascii letters at all.
"""

app = Client("my_account")
app.start()

target = "pyrogramchat"  # Target channel/supergroup username or id
users = {}  # To ensure uniqueness, users will be stored in a dictionary with user_id as key
limit = 200  # Amount of users to retrieve for each API call (200 is the maximum)

# "" + "0123456789" + "abcdefghijklmnopqrstuvwxyz" (as list)
queries = [""] + [str(i) for i in range(10)] + list(ascii_lowercase)

for q in queries:
    print("Searching for '{}'".format(q))
    offset = 0  # For each query, offset restarts from 0

    while True:
        try:
            participants = app.send(
                functions.channels.GetParticipants(
                    channel=app.resolve_peer(target),
                    filter=types.ChannelParticipantsSearch(q),
                    offset=offset,
                    limit=limit,
                    hash=0
                )
            )
        except FloodWait as e:
            # Very large chats could trigger FloodWait.
            # When happens, wait X seconds before continuing
            print("Flood wait: {} seconds".format(e.x))
            time.sleep(e.x)
            continue

        if not participants.participants:
            print("Done searching for '{}'".format(q))
            print()
            break  # No more participants left

        # User information are stored in the participants.users list.
        # Add those users to the dictionary
        users.update({i.id: i for i in participants.users})

        offset += len(participants.participants)

        print("Total users: {}".format(len(users)))

app.stop()

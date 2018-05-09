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
from pyrogram.api import functions
from pyrogram.api.errors import FloodWait

"""This example shows how to retrieve the full message history of a chat"""

app = Client("my_account")
app.start()

target = "me"  # "me" refers to your own chat (Saved Messages)
history = []  # List that will contain all the messages of the target chat
limit = 100  # Amount of messages to retrieve for each API call
offset = 0  # Offset starts at 0

while True:
    try:
        messages = app.send(
            functions.messages.GetHistory(
                app.resolve_peer(target),
                0, 0, offset, limit, 0, 0, 0
            )
        )
    except FloodWait as e:
        # For very large chats the method call can raise a FloodWait
        time.sleep(e.x)  # Sleep X seconds before continuing
        continue

    if not messages.messages:
        break  # No more messages left

    history.extend(messages.messages)
    offset += limit

app.stop()

# Now the "history" list contains all the messages sorted by date in
# descending order (from the most recent to the oldest one)

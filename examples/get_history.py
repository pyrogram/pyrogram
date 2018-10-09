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

"""This example shows how to retrieve the full message history of a chat"""

app = Client("my_account")
target = "me"  # "me" refers to your own chat (Saved Messages)
messages = []  # List that will contain all the messages of the target chat
offset_id = 0  # ID of the last message of the chunk

app.start()

while True:
    try:
        m = app.get_history(target, offset_id=offset_id)
    except FloodWait as e:  # For very large chats the method call can raise a FloodWait
        print("waiting {}".format(e.x))
        time.sleep(e.x)  # Sleep X seconds before continuing
        continue

    if not m.messages:
        break

    messages += m.messages
    offset_id = m.messages[-1].message_id

    print("Messages: {}".format(len(messages)))

app.stop()

# Now the "messages" list contains all the messages sorted by date in
# descending order (from the most recent to the oldest one)

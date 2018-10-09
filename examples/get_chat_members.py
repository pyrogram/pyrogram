"""This example shows you how to get the first 10.000 members of a chat.
Refer to get_chat_members2.py for more than 10.000 members.
"""

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

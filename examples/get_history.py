"""This example shows how to retrieve the full message history of a chat"""

import time

from pyrogram import Client
from pyrogram.api.errors import FloodWait

app = Client("my_account")
target = "me"  # "me" refers to your own chat (Saved Messages)
messages = []  # List that will contain all the messages of the target chat
offset_id = 0  # ID of the last message of the chunk

with app:
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

# Now the "messages" list contains all the messages sorted by date in
# descending order (from the most recent to the oldest one)

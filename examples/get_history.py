import time

from pyrogram import Client
from pyrogram.api import functions
from pyrogram.api.errors import FloodWait

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

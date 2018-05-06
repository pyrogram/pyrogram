import time

from pyrogram import Client
from pyrogram.api import functions, types
from pyrogram.api.errors import FloodWait

"""This simple GetParticipants method usage shows you how to get the first 10.000 users of a chat.

Refer to get_participants2.py for more than 10.000 users.
"""

app = Client("my_account")
app.start()

target = "pyrogramchat"  # Target channel/supergroup
users = []  # List that will contain all the users of the target chat
limit = 200  # Amount of users to retrieve for each API call
offset = 0  # Offset starts at 0

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

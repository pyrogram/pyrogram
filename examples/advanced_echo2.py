from pyrogram import Client
from pyrogram.api import types

"""This example is similar to advanced_echo.py, except for the fact that it will reply to Supergroup text messages only.

Beware! This script will make you reply to ALL new messages in every single supergroup you are in.
Make sure you add an extra check to filter them:

# Filter Supergroups by ID
if message.to_id.channel_id == MY_SUPERGROUP_ID:
    ...

# Filter Supergroups by Username
if chats[message.to_id.channel_id].username == MY_SUPERGROUP_USERNAME:
    ...
"""


def update_handler(client, update, users, chats):
    # Channels and Supergroups share the same type (Channel). The .megagroup field is used to tell them apart, and is
    # True for Supegroups, False for Channels.
    if isinstance(update, types.UpdateNewChannelMessage):  # Filter by UpdateNewChannelMessage (Channels/Supergroups)
        message = update.message

        if isinstance(message, types.Message):  # Filter by Message to exclude MessageService and MessageEmpty
            if chats[message.to_id.channel_id].megagroup:  # Only handle messages from Supergroups not Channels
                text = '[{}](tg://user?id={}) said "{}" in **{}** supergroup'.format(
                    users[message.from_id].first_name,
                    users[message.from_id].id,
                    message.message,
                    chats[message.to_id.channel_id].title
                )

                client.send_message(
                    message.to_id,
                    text,
                    reply_to_message_id=message.id
                )


def main():
    # Pyrogram setup
    client = Client("example")

    # Set the update_handler callback function
    client.set_update_handler(update_handler)
    client.start()

    # Blocks the program execution until you press CTRL+C then
    # automatically stops the Client by closing the underlying connection
    client.idle()


if __name__ == "__main__":
    main()

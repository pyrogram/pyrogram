from pyrogram import Client
from pyrogram.api import types

"""This is a more advanced example bot that will reply to all private and basic groups text messages
by also mentioning the Users.

Beware! This script will make you reply to ALL new messages in private chats and in every basic group you are in.
Make sure you add an extra check to filter them:

# Filter Groups by ID
if message.to_id.chat_id == MY_GROUP_ID:
    ...
"""


def update_handler(client, update, users, chats):
    if isinstance(update, types.UpdateNewMessage):  # Filter by UpdateNewMessage (PM and Chats)
        message = update.message

        if isinstance(message, types.Message):  # Filter by Message to exclude MessageService and MessageEmpty
            if isinstance(message.to_id, types.PeerUser):  # Private Messages
                text = '[{}](tg://user?id={}) said "{}" to me ([{}](tg://user?id={}))'.format(
                    users[message.from_id].first_name,
                    users[message.from_id].id,
                    message.message,
                    users[message.to_id.user_id].first_name,
                    users[message.to_id.user_id].id
                )

                client.send_message(
                    message.from_id,  # Send the message to the private chat (from_id)
                    text,
                    reply_to_message_id=message.id
                )
            else:  # Group chats
                text = '[{}](tg://user?id={}) said "{}" in **{}** group'.format(
                    users[message.from_id].first_name,
                    users[message.from_id].id,
                    message.message,
                    chats[message.to_id.chat_id].title
                )

                client.send_message(
                    message.to_id,  # Send the message to the group chat (to_id)
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

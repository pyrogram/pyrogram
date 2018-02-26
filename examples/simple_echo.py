from pyrogram import Client
from pyrogram.api import types

"""This simple example bot will reply to all private text messages"""


def update_handler(client, update, users, chats):
    if isinstance(update, types.UpdateNewMessage):  # Filter by UpdateNewMessage (Private Messages)
        message = update.message  # type: types.Message

        if isinstance(message, types.Message):  # Filter by Message to exclude MessageService and MessageEmpty
            if isinstance(message.to_id, types.PeerUser):  # Private Messages (Message from user)
                client.send_message(
                    chat_id=message.from_id,
                    text=message.message,
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

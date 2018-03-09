from pyrogram import Client


# This function will be called every time a new Update is received from Telegram
def update_handler(client, update, users, chats):
    # Send EVERY update that arrives to your own chat (Saved Messages)
    # Use triple backticks to make the text look nicer.
    client.send_message("me", "```\n" + str(update) + "```")


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

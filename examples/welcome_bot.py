from pyrogram import Client, Emoji
from pyrogram.api import types

"""
This is the Welcome Bot in @PyrogramChat
The code is commented to help you understand each part

It also uses the Emoji module to easily add emojis in your text messages
"""

# Your Supergroup ID
SUPERGROUP_ID = 1387666944


def update_handler(client, update, users, chats):
    # Supergroup messages are contained in the "UpdateNewChannelMessage" update type
    if isinstance(update, types.UpdateNewChannelMessage):
        message = update.message
        # When a user joins, a "MessageService" is received
        if isinstance(message, types.MessageService):
            # Check if the message is sent to your SUPERGROUP_ID
            if message.to_id.channel_id == SUPERGROUP_ID:
                # A "MessageService" contains the "action" field.
                # The action for user joins is "MessageActionChatAddUser" if the user
                # joined using the username, otherwise is "MessageActionChatJoinedByLink" if
                # the user joined a private group by link
                if isinstance(message.action, (types.MessageActionChatAddUser, types.MessageActionChatJoinedByLink)):
                    # Now send the welcome message. Extra info about a user (such as the first_name, username, ...)
                    # are contained in the users dictionary and can be accessed by the user ID
                    client.send_message(
                        SUPERGROUP_ID,
                        "{} Welcome to [Pyrogram](https://docs.pyrogram.ml/)'s "
                        "group chat, [{}](tg://user?id={})!".format(
                            Emoji.SPARKLES,  # Add an emoji
                            users[message.from_id].first_name,
                            users[message.from_id].id
                        ),
                        reply_to_message_id=message.id,
                        disable_web_page_preview=True
                    )


def main():
    client = Client("example")
    client.set_update_handler(update_handler)

    client.start()
    client.idle()


if __name__ == "__main__":
    main()

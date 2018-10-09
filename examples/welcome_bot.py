"""This is the Welcome Bot in @PyrogramChat.

It uses the Emoji module to easily add emojis in your text messages and Filters
to make it only work for specific messages in a specific chat.
"""

from pyrogram import Client, Emoji, Filters

MENTION = "[{}](tg://user?id={})"
MESSAGE = "{} Welcome to [Pyrogram](https://docs.pyrogram.ml/)'s group chat {}!"

app = Client("my_account")


@app.on_message(Filters.chat("PyrogramChat") & Filters.new_chat_members)
def welcome(client, message):
    # Build the new members list (with mentions) by using their first_name
    new_members = [MENTION.format(i.first_name, i.id) for i in message.new_chat_members]

    # Build the welcome message by using an emoji and the list we built above
    text = MESSAGE.format(Emoji.SPARKLES, ", ".join(new_members))

    # Send the welcome message
    message.reply(text, disable_web_page_preview=True)


app.run()  # Automatically start() and idle()

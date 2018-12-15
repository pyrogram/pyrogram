"""This is the Welcome Bot in @PyrogramChat.

It uses the Emoji module to easily add emojis in your text messages and Filters
to make it only work for specific messages in a specific chat.
"""

from pyrogram import Client, Emoji, Filters

USER = "**{}**"
MESSAGE = "{} Welcome to [Pyrogram](https://docs.pyrogram.ml/)'s group chat {{}}!".format(Emoji.SPARKLES)

enabled_groups = Filters.chat("PyrogramChat")
last_welcomes = {}

app = Client("my_account")


@app.on_message(enabled_groups & Filters.new_chat_members)
def welcome(client, message):
    chat_id = message.chat.id

    # Get the previous welcome message and members, if any
    previous_welcome, previous_members = last_welcomes.pop(chat_id, (None, []))

    # Delete the previous message, if exists
    if previous_welcome:
        previous_welcome.delete()

    # Build the new members list by using their first_name. Also append the previous members, if any
    new_members = [USER.format(i.first_name) for i in message.new_chat_members] + previous_members

    # Build the welcome message by using an emoji and the list we created above
    text = MESSAGE.format(", ".join(new_members))

    # Actually send the welcome and save the new message and the new members list
    last_welcomes[message.chat.id] = message.reply(text, disable_web_page_preview=True), new_members


@app.on_message(enabled_groups)
def reset(client, message):
    # Don't make the bot delete the previous welcome in case someone talks in the middle
    last_welcomes.pop(message.chat.id, None)


app.run()  # Automatically start() and idle()

from pyrogram import Client, Emoji, Filters

"""This is the Welcome Bot in @PyrogramChat.

It uses the Emoji module to easily add emojis in your text messages and Filters
to make it only work for specific messages in a specific chat 
"""

app = Client("my_account")


@app.on_message(Filters.chat("PyrogramChat") & Filters.new_chat_members)
def welcome(client, message):
    # Build the new members list (with mentions) by using their first_name
    new_members = ", ".join([
        "[{}](tg://user?id={})".format(i.first_name, i.id)
        for i in message.new_chat_members
    ])

    # Build the welcome message by using an emoji and the list we built above
    text = "{} Welcome to [Pyrogram](https://docs.pyrogram.ml/)'s group chat {}!".format(
        Emoji.SPARKLES,
        new_members
    )

    # Send the welcome message
    client.send_message(
        message.chat.id, text,
        reply_to_message_id=message.message_id,
        disable_web_page_preview=True
    )


app.run()  # Automatically start() and idle()

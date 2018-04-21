from pyrogram import Client, Emoji, Filters

"""
This is the Welcome Bot in @PyrogramChat
It uses the Emoji module to easily add emojis in your text messages and Filters
to make it only work for specific messages in a specific chat 
"""

app = Client("my_account")


@app.on_message(Filters.chat("PyrogramChat") & Filters.new_chat_members)
def welcome(client, message):
    new_members = ", ".join([
        "[{}](tg://user?id={})".format(i.first_name, i.id)
        for i in message.new_chat_members
    ])

    text = "{} Welcome to [Pyrogram](https://docs.pyrogram.ml/)'s group chat {}!".format(
        Emoji.SPARKLES,
        new_members
    )

    client.send_message(
        message.chat.id, text,
        reply_to_message_id=message.message_id,
        disable_web_page_preview=True
    )


app.start()
app.idle()

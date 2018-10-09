"""This simple echo bot replies to every private text message.

It uses the @on_message decorator to register a MessageHandler and applies two filters on it:
Filters.text and Filters.private to make sure it will reply to private text messages only.
"""

from pyrogram import Client, Filters

app = Client("my_account")


@app.on_message(Filters.text & Filters.private)
def echo(client, message):
    message.reply(message.text, quote=True)


app.run()  # Automatically start() and idle()

welcomebot
==========

This example uses the ``emoji`` module to easily add emoji in your text messages and ``filters``
to make it only work for specific messages in a specific chat.

.. code-block:: python

    from pyrogram import Client, emoji, filters

    TARGET = -100123456789  # Target chat. Can also be a list of multiple chat ids/usernames
    MENTION = "[{}](tg://user?id={})"  # User mention markup
    MESSAGE = "{} Welcome to [Pyrogram](https://docs.pyrogram.org/)'s group chat {}!"  # Welcome message

    app = Client("my_account")


    # Filter in only new_chat_members updates generated in TARGET chat
    @app.on_message(filters.chat(TARGET) & filters.new_chat_members)
    def welcome(client, message):
        # Build the new members list (with mentions) by using their first_name
        new_members = [u.mention for u in message.new_chat_members]

        # Build the welcome message by using an emoji and the list we built above
        text = MESSAGE.format(emoji.SPARKLES, ", ".join(new_members))

        # Send the welcome message, without the web page preview
        message.reply_text(text, disable_web_page_preview=True)


    app.run()  # Automatically start() and idle()
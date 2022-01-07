echobot
=======

This simple echo bot replies to every private text message.

It uses the ``@on_message`` decorator to register a ``MessageHandler`` and applies two filters on it:
``filters.text`` and ``filters.private`` to make sure it will reply to private text messages only.

.. code-block:: python

    from pyrogram import Client, filters

    app = Client("my_account")


    @app.on_message(filters.text & filters.private)
    def echo(client, message):
        message.reply(message.text)


    app.run()  # Automatically start() and idle()
hello_world
===========

This example demonstrates a basic API usage

.. code-block:: python

    from pyrogram import Client

    # Create a new Client instance
    app = Client("my_account")

    with app:
        # Send a message, Markdown is enabled by default
        app.send_message("me", "Hi there! I'm using **Pyrogram**")

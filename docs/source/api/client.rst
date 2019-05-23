Pyrogram Client
===============

This is the Client class. It exposes high-level methods for an easy access to the API.

.. code-block:: python
    :emphasize-lines: 1-3

    from pyrogram import Client

    app = Client("my_account")

    with app:
        app.send_message("me", "Hi!")

.. autoclass:: pyrogram.Client()

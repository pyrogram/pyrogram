get_history
===========

This example shows how to get the full message history of a chat, starting from the latest message.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")
    target = "me"  # "me" refers to your own chat (Saved Messages)

    with app:
        for message in app.iter_history(target):
            print(message.text)
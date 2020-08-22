raw_updates
===========

This example shows how to handle raw updates.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")


    @app.on_raw_update()
    def raw(client, update, users, chats):
        print(update)


    app.run()  # Automatically start() and idle()

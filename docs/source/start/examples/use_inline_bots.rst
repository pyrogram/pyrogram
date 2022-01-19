use_inline_bots
===============

This example shows how to query an inline bot (as user).

.. code-block:: python

    from pyrogram import Client

    # Create a new Client
    app = Client("my_account")

    with app:
        # Get bot results for "hello" from the inline bot @vid
        bot_results = app.get_inline_bot_results("vid", "hello")

        # Send the first result (bot_results.results[0]) to your own chat (Saved Messages)
        app.send_inline_bot_result("me", bot_results.query_id, bot_results.results[0].id)
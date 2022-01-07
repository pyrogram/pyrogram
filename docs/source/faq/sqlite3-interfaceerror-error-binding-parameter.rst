sqlite3.InterfaceError: Error binding parameter
===============================================

This error occurs when you pass a chat id value of the wrong type when trying to call a method. Most likely, you
accidentally passed the whole user or chat object instead of the id or username.

.. code-block:: python

    # Wrong. You passed the whole Chat instance
    app.send_message(chat, "text")

    # Correct
    app.send_message(chat.id, "text")
Update Handling
===============

Updates are events that happen in your Telegram account (incoming messages, new channel posts, user name changes, ...)
and can be handled by using a callback function, that is, a function called every time an ``Update`` is received from
Telegram.

To set an update handler simply call :meth:`set_update_handler <pyrogram.Client.set_update_handler>`
by passing the name of your defined callback function as argument *before* you start the Client.

Here's a complete example on how to set it up:

.. code-block:: python

    from pyrogram import Client


    def update_handler(client, update, users, chats):
        print(update)

    def main():
        client = Client(session_name="example")
        client.set_update_handler(update_handler)

        client.start()
        client.idle()

    if __name__ == "__main__":
        main()

The last line of the main function, :meth:`client.idle() <pyrogram.Client.idle>`, is not strictly necessary but highly
recommended when using the update handler; it will block your script execution until you press ``CTRL+C`` and
automatically call the :meth:`stop <pyrogram.Client.stop>` method which stops the Client and gently close the underlying
connection.

Examples
--------

- `Simple Echo <https://github.com/pyrogram/pyrogram/blob/master/examples/simple_echo.py>`_
- `Advanced Echo <https://github.com/pyrogram/pyrogram/blob/master/examples/advanced_echo.py>`_
- `Advanced Echo 2 <https://github.com/pyrogram/pyrogram/blob/master/examples/advanced_echo2.py>`_

Usage
=====

Having your `project set up`_ and your account authorized_, it's time to play with the API. Let's start!

High-level API
--------------

The easiest and recommended way to interact with Telegram is via the high-level Pyrogram methods_ and types_, which are
named after the `Telegram Bot API`_.

Here's a simple example:

    .. code-block:: python

        from pyrogram import Client

        app = Client("my_account")

        app.start()

        print(app.get_me())
        app.send_message("me", "Hi there! I'm using **Pyrogram**")
        app.send_location("me", 51.500729, -0.124583)

        app.stop()

You can also use Pyrogram in a context manager with the ``with`` statement. The Client will automatically
:meth:`start <pyrogram.Client.start>` and :meth:`stop <pyrogram.Client.stop>` gracefully, even in case of unhandled
exceptions in your code:

    .. code-block:: python

        from pyrogram import Client

        app = Client("my_account")

        with app:
            print(app.get_me())
            app.send_message("me", "Hi there! I'm using **Pyrogram**")
            app.send_location("me", 51.500729, -0.124583)

More examples on `GitHub <https://github.com/pyrogram/pyrogram/tree/develop/examples>`_.

.. _project set up: Setup.html
.. _authorized: Setup.html#user-authorization
.. _Telegram Bot API: https://core.telegram.org/bots/api
.. _methods: ../pyrogram/Client.html#messages
.. _types: ../pyrogram/Types.html
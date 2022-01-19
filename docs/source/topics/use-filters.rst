Using Filters
=============

So far we've seen :doc:`how to register a callback function <../start/updates>` that executes every time an update comes
from the server, but there's much more than that to come.

Here we'll discuss about :obj:`~pyrogram.filters`. Filters enable a fine-grain control over what kind of
updates are allowed or not to be passed in your callback functions, based on their inner details.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Single Filters
--------------

Let's start right away with a simple example:

-   This example will show you how to **only** handle messages containing a :class:`~pyrogram.types.Sticker` object and
    ignore any other message. Filters are passed as the first argument of the decorator:

    .. code-block:: python

        from pyrogram import filters


        @app.on_message(filters.sticker)
        def my_handler(client, message):
            print(message)

-   or, without decorators. Here filters are passed as the second argument of the handler constructor; the first is the
    callback function itself:

    .. code-block:: python

        from pyrogram import filters
        from pyrogram.handlers import MessageHandler


        def my_handler(client, message):
            print(message)


        app.add_handler(MessageHandler(my_handler, filters.sticker))

Combining Filters
-----------------

Filters can be used in a more advanced way by inverting and combining more filters together using bitwise
operators ``~``, ``&`` and ``|``:

-   Use ``~`` to invert a filter (behaves like the ``not`` operator).
-   Use ``&`` and ``|`` to merge two filters (behave like ``and``, ``or`` operators respectively).

Here are some examples:

-   Message is a **text** message **and** is **not edited**.

    .. code-block:: python

        @app.on_message(filters.text & ~filters.edited)
        def my_handler(client, message):
            print(message)

-   Message is a **sticker** **and** is coming from a **channel or** a **private** chat.

    .. code-block:: python

        @app.on_message(filters.sticker & (filters.channel | filters.private))
        def my_handler(client, message):
            print(message)

Advanced Filters
----------------

Some filters, like :meth:`~pyrogram.filters.command` or :meth:`~pyrogram.filters.regex`
can also accept arguments:

-   Message is either a */start* or */help* **command**.

    .. code-block:: python

        @app.on_message(filters.command(["start", "help"]))
        def my_handler(client, message):
            print(message)

-   Message is a **text** message or a media **caption** matching the given **regex** pattern.

    .. code-block:: python

        @app.on_message(filters.regex("pyrogram"))
        def my_handler(client, message):
            print(message)

More handlers using different filters can also live together.

.. code-block:: python

    @app.on_message(filters.command("start"))
    def start_command(client, message):
        print("This is the /start command")


    @app.on_message(filters.command("help"))
    def help_command(client, message):
        print("This is the /help command")


    @app.on_message(filters.chat("PyrogramChat"))
    def from_pyrogramchat(client, message):
        print("New message in @PyrogramChat")

Using Filters
=============

So far we've seen :doc:`how to register a callback function <../start/updates>` that executes every time a specific update
comes from the server, but there's much more than that to come.

Here we'll discuss about :class:`~pyrogram.Filters`. Filters enable a fine-grain control over what kind of
updates are allowed or not to be passed in your callback functions, based on their inner details.

.. contents:: Contents
    :backlinks: none
    :local:

-----

Single Filters
--------------

Let's start right away with a simple example:

-   This example will show you how to **only** handle messages containing an :class:`~pyrogram.Audio` object and
    ignore any other message. Filters are passed as the first argument of the decorator:

    .. code-block:: python
        :emphasize-lines: 4

        from pyrogram import Filters


        @app.on_message(Filters.audio)
        def my_handler(client, message):
            print(message)

-   or, without decorators. Here filters are passed as the second argument of the handler constructor; the first is the
    callback function itself:

    .. code-block:: python
        :emphasize-lines: 8

        from pyrogram import Filters, MessageHandler


        def my_handler(client, message):
            print(message)


        app.add_handler(MessageHandler(my_handler, Filters.audio))

Combining Filters
-----------------

Filters can also be used in a more advanced way by inverting and combining more filters together using bitwise
operators ``~``, ``&`` and ``|``:

-   Use ``~`` to invert a filter (behaves like the ``not`` operator).
-   Use ``&`` and ``|`` to merge two filters (behave like ``and``, ``or`` operators respectively).

Here are some examples:

-   Message is a **text** message **and** is **not edited**.

    .. code-block:: python

        @app.on_message(Filters.text & ~Filters.edited)
        def my_handler(client, message):
            print(message)

-   Message is a **sticker** **and** is coming from a **channel or** a **private** chat.

    .. code-block:: python

        @app.on_message(Filters.sticker & (Filters.channel | Filters.private))
        def my_handler(client, message):
            print(message)

Advanced Filters
----------------

Some filters, like :meth:`~pyrogram.Filters.command` or :meth:`~pyrogram.Filters.regex`
can also accept arguments:

-   Message is either a */start* or */help* **command**.

    .. code-block:: python

        @app.on_message(Filters.command(["start", "help"]))
        def my_handler(client, message):
            print(message)

-   Message is a **text** message or a media **caption** matching the given **regex** pattern.

    .. code-block:: python

        @app.on_message(Filters.regex("pyrogram"))
        def my_handler(client, message):
            print(message)

More handlers using different filters can also live together.

.. code-block:: python

    @app.on_message(Filters.command("start"))
    def start_command(client, message):
        print("This is the /start command")


    @app.on_message(Filters.command("help"))
    def help_command(client, message):
        print("This is the /help command")


    @app.on_message(Filters.chat("PyrogramChat"))
    def from_pyrogramchat(client, message):
        print("New message in @PyrogramChat")

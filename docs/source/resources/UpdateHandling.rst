Update Handling
===============

Updates are handled by registering one or more callback functions with an Handler.
There are multiple Handlers to choose from, one for each kind of update.

Registering an Handler
----------------------

We shall examine the :obj:`MessageHandler <pyrogram.MessageHandler>`, which will be in charge for handling
:obj:`Message <pyrogram.api.types.pyrogram.Message>` objects.

The easiest and nicest way to register a MessageHandler is by decorating your function with the
:meth:`on_message() <pyrogram.Client.on_message>` decorator. Here's a full example that prints out the content
of a message as soon as it arrives.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")


    @app.on_message()
    def my_handler(client, message):
        print(message)


    app.start()
    app.idle()

Alternatively, if you prefer not to use decorators, there is an alternative way for registering Handlers.
This is useful, for example, if you want to keep your callback functions in a separate file.

.. code-block:: python

    from pyrogram import Client, MessageHandler

    def my_handler(client, message):
        print(message)

    app = Client("my_account")

    app.add_handler(MessageHandler(my_handler))

    app.start()
    app.idle()

Using Filters
-------------

For a finer grained control over what kind of messages will be allowed or not, you can use
:class:`Filters <pyrogram.Filters>`. The next example will show you how to handler only messages
containing an :obj:`Audio <pyrogram.api.types.pyrogram.Audio>` object:

.. code-block:: python

    from pyrogram import Filters

    @app.on_message(Filters.audio)
    def my_handler(client, message):
        print(message)

or, without decorators:

.. code-block:: python

    from pyrogram import Filters, Messagehandler

    def my_handler(client, message):
        print(message)

    app.add_handler(MessageHandler(my_handler, Filters.audio))

Advanced Filters
----------------

Filters can also be used in a more advanced way by combining more filters together using bitwise operators:

-   Use ``~`` to invert a filter (behaves like the ``not`` operator).
-   Use ``&`` and ``|`` to merge two filters (``and``, ``or`` operators respectively).

Here are some examples:

-   Message is a **text** message **and** is **not edited**.

    .. code-block:: python

        @app.on_message(Filters.text & ~Filters.edited)
        def my_handler(client, message):
            print(message)

-   Message is a **sticker** **and** was sent in a **channel** or in a **private** chat.

    .. code-block:: python

        @app.on_message(Filters.sticker & (Filters.channel | Filters.private))
        def my_handler(client, message):
            print(message)

Some filters can also accept parameters, like :obj:`command <pyrogram.Filters.command>` or
:obj:`regex <pyrogram.Filters.regex>`:

-   Message is either a /start or /help **command**.

    .. code-block:: python

        @app.on_message(Filters.command(["start", "help"]))
        def my_handler(client, message):
            print(message)

-   Message is a **text** message matching the given regex pattern.

    .. code-block:: python

        @app.on_message(Filters.regex("pyrogram"))
        def my_handler(client, message):
            print(message)
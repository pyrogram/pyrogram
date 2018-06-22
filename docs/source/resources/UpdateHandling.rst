Update Handling
===============

Updates are events that happen in your Telegram account (incoming messages, new channel posts, new members join, ...)
and are handled by registering one or more callback functions with an Handler. There are multiple Handlers to choose
from, one for each kind of update:

-   `MessageHandler <../pyrogram/handlers/MessageHandler.html>`_
-   `DeletedMessagesHandler <../pyrogram/handlers/DeletedMessagesHandler.html>`_
-   `CallbackQueryHandler <../pyrogram/handlers/CallbackQueryHandler.html>`_
-   `RawUpdateHandler <../pyrogram/handlers/RawUpdateHandler.html>`_

Registering an Handler
----------------------

We shall examine the :obj:`MessageHandler <pyrogram.MessageHandler>`, which will be in charge for handling
:obj:`Message <pyrogram.Message>` objects.

-   The easiest and nicest way to register a MessageHandler is by decorating your function with the
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

-   If you prefer not to use decorators, there is an alternative way for registering Handlers.
    This is useful, for example, when you want to keep your callback functions in separate files.

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

For a finer grained control over what kind of messages will be allowed or not in your callback functions, you can use
:class:`Filters <pyrogram.Filters>`.

-   This example will show you how to **only** handle messages containing an
    :obj:`Audio <pyrogram.Audio>` object and filter out any other message:

    .. code-block:: python

        from pyrogram import Filters


        @app.on_message(Filters.audio)
        def my_handler(client, message):
            print(message)

-   or, without decorators:

    .. code-block:: python

        from pyrogram import Filters, MessageHandler


        def my_handler(client, message):
            print(message)


        app.add_handler(MessageHandler(my_handler, Filters.audio))

Combining Filters
-----------------

Filters can also be used in a more advanced way by combining more filters together using bitwise operators:

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

Some filters, like :obj:`command() <pyrogram.Filters.command>` or :obj:`regex() <pyrogram.Filters.regex>`
can also accept arguments:

-   Message is either a */start* or */help* **command**.

    .. code-block:: python

        @app.on_message(Filters.command(["start", "help"]))
        def my_handler(client, message):
            print(message)

-   Message is a **text** message matching the given **regex** pattern.

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

Handler Groups
--------------

If you register handlers with overlapping filters, only the first one is executed and any other handler will be ignored.

In order to process the same message more than once, you can register your handler in a different group.
Groups are identified by a number (number 0 being the default) and are sorted. This means that a lower group number has
a higher priority.

For example, in:

.. code-block:: python

    @app.on_message(Filters.text | Filters.sticker)
    def text_or_sticker(client, message):
        print("Text or Sticker")


    @app.on_message(Filters.text)
    def just_text(client, message):
        print("Just Text")

``just_text`` is never executed. To enable it, simply register the function using a different group:

.. code-block:: python

    @app.on_message(Filters.text, group=1)
    def just_text(client, message):
        print("Just Text")

or, if you want ``just_text`` to be fired *before* ``text_or_sticker``:

.. code-block:: python

    @app.on_message(Filters.text, group=-1)
    def just_text(client, message):
        print("Just Text")
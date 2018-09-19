Using Filters
=============

For a finer grained control over what kind of messages will be allowed or not in your callback functions, you can use
:class:`Filters <pyrogram.Filters>`.

.. note::
    This section makes use of Handlers to handle updates. Learn more at `Update Handling <UpdateHandling.html>`_.

-   This example will show you how to **only** handle messages containing an :obj:`Audio <pyrogram.Audio>` object and
    ignore any other message:

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

Filters can also be used in a more advanced way by inverting and combining more filters together using bitwise
operators:

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

Some filters, like :meth:`command() <pyrogram.Filters.command>` or :meth:`regex() <pyrogram.Filters.regex>`
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

``just_text`` is never executed because ``text_or_sticker`` already handles texts. To enable it, simply register the
function using a different group:

.. code-block:: python

    @app.on_message(Filters.text, group=1)
    def just_text(client, message):
        print("Just Text")

or, if you want ``just_text`` to be fired *before* ``text_or_sticker`` (note ``-1``, which is less than ``0``):

.. code-block:: python

    @app.on_message(Filters.text, group=-1)
    def just_text(client, message):
        print("Just Text")

Custom Filters
--------------

Pyrogram already provides lots of built-in :class:`Filters <pyrogram.Filters>` to work with, but in case you can't find
a specific one for your needs or want to build a custom filter by yourself (to be used in a different handler, for
example) you can use :meth:`Filters.create() <pyrogram.Filters.create>`.

.. note::
    At the moment, the built-in filters are intended to be used with the :obj:`MessageHandler <pyrogram.MessageHandler>`
    only.

An example to demonstrate how custom filters work is to show how to create and use one for the
:obj:`CallbackQueryHandler <pyrogram.CallbackQueryHandler>`. Note that callback queries updates are only received by Bots;
create and `authorize your bot <../start/Setup.html#bot-authorization>`_, then send a message with an inline keyboard to
yourself. This allows you to test your filter by pressing the inline button:

.. code-block:: python

    from pyrogram import InlineKeyboardMarkup, InlineKeyboardButton

    app.send_message(
        "username",  # Change this to your username or id
        "Pyrogram's custom filter test",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Press me", "pyrogram")]]
        )
    )

Basic Filters
^^^^^^^^^^^^^

For this basic filter we will be using only the first two parameters of :meth:`Filters.create() <pyrogram.Filters.create>`.

The code below creates a simple filter for hardcoded callback data. This filter will only allow callback queries
containing "pyrogram" as data:

.. code-block:: python

    hardcoded_data = Filters.create(
        name="HardcodedData",
        func=lambda filter, callback_query: callback_query.data == "pyrogram"
    )

The ``lambda`` operator in python is used to create small anonymous functions and is perfect for this example, the same
could be achieved with a normal function, but we don't really need it as it makes sense only inside the filter itself:

.. code-block:: python

    def func(filter, callback_query):
        return callback_query.data == "pyrogram"

    hardcoded_data = Filters.create(
        name="HardcodedData",
        func=func
    )

The filter usage remains the same:

.. code-block:: python

    @app.on_callback_query(hardcoded_data)
    def pyrogram_data(client, callback_query):
        client.answer_callback_query(callback_query.id, "it works!")

Filters with Arguments
^^^^^^^^^^^^^^^^^^^^^^

A much cooler filter would be one that accepts "pyrogram" or any other data as argument at usage time.
A dynamic filter like this will make use of the third parameter of :meth:`Filters.create() <pyrogram.Filters.create>`.

This is how a dynamic custom filter looks like:

.. code-block:: python

    def dynamic_data(data):
        return Filters.create(
            name="DynamicData",
            func=lambda filter, callback_query: filter.data == callback_query.data,
            data=data  # "data" kwarg is accessed with "filter.data"
        )

And its usage:

.. code-block:: python

    @app.on_callback_query(dynamic_data("pyrogram"))
    def pyrogram_data(client, callback_query):
        client.answer_callback_query(callback_query.id, "it works!")
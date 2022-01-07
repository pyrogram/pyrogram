Creating Filters
================

Pyrogram already provides lots of built-in :class:`~pyrogram.filters` to work with, but in case you can't find a
specific one for your needs or want to build a custom filter by yourself you can use
:meth:`filters.create() <pyrogram.filters.create>`.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Custom Filters
--------------

An example to demonstrate how custom filters work is to show how to create and use one for the
:class:`~pyrogram.handlers.CallbackQueryHandler`. Note that callback queries updates are only received by bots as result
of a user pressing an inline button attached to the bot's message; create and :doc:`authorize your bot <../start/auth>`,
then send a message with an inline keyboard to yourself. This allows you to test your filter by pressing the inline
button:

.. code-block:: python

    from pyrogram.types import InlineKeyboardMarkup, InlineKeyboardButton

    app.send_message(
        "username",  # Change this to your username or id
        "Pyrogram custom filter test",
        reply_markup=InlineKeyboardMarkup(
            [[InlineKeyboardButton("Press me", "pyrogram")]]
        )
    )

Basic Filters
-------------

For this basic filter we will be using only the first parameter of :meth:`~pyrogram.filters.create`.

The heart of a filter is its callback function, which accepts three arguments *(self, client, update)* and returns
either ``True``, in case you want the update to pass the filter or ``False`` otherwise.

In this example we are matching the query data to "pyrogram", which means that the filter will only allow callback
queries containing "pyrogram" as data:

.. code-block:: python

    from pyrogram import filters

    static_data_filter = filters.create(lambda _, __, query: query.data == "pyrogram")

The first two arguments of the callback function are unused here and because of this we named them using underscores.

The ``lambda`` operator in python is used to create small anonymous functions and is perfect for this example. The same
can be achieved with a normal function, but we don't really need it as it makes sense only inside the filter's scope:

.. code-block:: python

    from pyrogram import filters

    def func(_, __, query):
        return query.data == "pyrogram"

    static_data_filter = filters.create(func)

Asynchronous filters are also possible. Sadly, Python itself doesn't have an ``async lambda``, so we are left with
using a named function:

.. code-block:: python

    from pyrogram import filters

    async def func(_, __, query):
        return query.data == "pyrogram"

    static_data_filter = filters.create(func)

Finally, the filter usage remains the same:

.. code-block:: python

    @app.on_callback_query(static_data_filter)
    def pyrogram_data(_, query):
        query.answer("it works!")

Filters with Arguments
----------------------

A more flexible filter would be one that accepts "pyrogram" or any other string as argument at usage time.
A dynamic filter like this will make use of named arguments for the :meth:`~pyrogram.filters.create` method and the
first argument of the callback function, which is a reference to the filter object itself holding the extra data passed
via named arguments.

This is how a dynamic custom filter looks like:

.. code-block:: python

    from pyrogram import filters

    def dynamic_data_filter(data):
        return filters.create(
            lambda flt, _, query: flt.data == query.data,
            data=data  # "data" kwarg is accessed with "flt.data" above
        )

And its asynchronous variant:

.. code-block:: python

    from pyrogram import filters

    def dynamic_data_filter(data):
        async def func(flt, _, query):
            return flt.data == query.data

        # "data" kwarg is accessed with "flt.data" above
        return filters.create(func, data=data)

And finally its usage:

.. code-block:: python

    @app.on_callback_query(dynamic_data_filter("pyrogram"))
    def pyrogram_data(_, query):
        query.answer("it works!")


Method Calls Inside Filters
---------------------------

The missing piece we haven't covered yet is the second argument of a filter callback function, namely, the ``client``
argument. This is a reference to the :obj:`~pyrogram.Client` instance that is running the filter and it is useful in
case you would like to make some API calls before deciding whether the filter should allow the update or not:

.. code-block:: python

    def func(_, client, query):
        # r = client.some_api_method()
        # check response "r" and decide to return True or False
        ...

Asynchronous filters making API calls work fine as well. Just remember that you need to put ``async`` in front of
function definitions and ``await`` in front of method calls:

.. code-block:: python

    async def func(_, client, query):
        # r = await client.some_api_method()
        # check response "r" and decide to return True or False
        ...
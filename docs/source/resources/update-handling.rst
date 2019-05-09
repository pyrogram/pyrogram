Update Handling
===============

Let's now dive right into the core of the framework.

Updates are events that happen in your Telegram account (incoming messages, new channel posts, new members join, ...)
and are handled by registering one or more callback functions in your app using `Handlers <../pyrogram/Handlers.html>`_.

Each handler deals with a specific event and once a matching update arrives from Telegram, your registered callback
function will be called.

Registering an Handler
----------------------

To explain how handlers work let's have a look at the most used one, the
:obj:`MessageHandler <pyrogram.MessageHandler>`, which will be in charge for handling :obj:`Message <pyrogram.Message>`
updates coming from all around your chats. Every other handler shares the same setup logic; you should not have troubles
settings them up once you learn from this section.

Using add_handler()
-------------------

The :meth:`add_handler() <pyrogram.Client.add_handler>` method takes any handler instance that wraps around your defined
callback function and registers it in your Client. Here's a full example that prints out the content of a message as
soon as it arrives:

.. code-block:: python

    from pyrogram import Client, MessageHandler


    def my_function(client, message):
        print(message)


    app = Client("my_account")

    my_handler = MessageHandler(my_function)
    app.add_handler(my_handler)

    app.run()

Using Decorators
----------------

A much nicer way to register a MessageHandler is by decorating your callback function with the
:meth:`on_message() <pyrogram.Client.on_message>` decorator, which will still make use of add_handler() under the hood.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")


    @app.on_message()
    def my_handler(client, message):
        print(message)


    app.run()


.. note::

    Due to how these decorators work in Pyrogram, they will wrap your defined callback function in a tuple consisting of
    ``(handler, group)``; this will be the value held by your function identifier (e.g.: *my_function* from the example
    above).

    In case, for some reason, you want to get your own function back after it has been decorated, you need to access
    ``my_function[0].callback``, that is, the *callback* field of the *handler* object which is the first element in the
    tuple.
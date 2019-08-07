Handling Updates
================

Calling :doc:`API methods <invoking>` sequentially is cool, but how to react when, for example, a new message arrives?
This page deals with updates and how to handle such events in Pyrogram. Let's have a look at how they work.

Defining Updates
----------------

First, let's define what are these updates. As hinted already, updates are simply events that happen in your Telegram
account (incoming messages, new members join, bot button presses, etc...), which are meant to notify you about a new
specific state that has changed. These updates are handled by registering one or more callback functions in your app
using :doc:`Handlers <../api/handlers>`.

Each handler deals with a specific event and once a matching update arrives from Telegram, your registered callback
function will be called back by the framework and its body executed.

Registering a Handler
---------------------

To explain how handlers work let's have a look at the most used one, the :class:`~pyrogram.MessageHandler`, which will
be in charge for handling :class:`~pyrogram.Message` updates coming from all around your chats. Every other handler shares
the same setup logic; you should not have troubles settings them up once you learn from this section.

Using add_handler()
-------------------

The :meth:`~pyrogram.Client.add_handler` method takes any handler instance that wraps around your defined callback
function and registers it in your Client. Here's a full example that prints out the content of a message as soon as it
arrives:

.. code-block:: python

    from pyrogram import Client, MessageHandler


    def my_function(client, message):
        print(message)


    app = Client("my_account")

    my_handler = MessageHandler(my_function)
    app.add_handler(my_handler)

    app.run()

Let's examine these four new pieces.

#.  A callback function we defined which accepts two arguments -
    *(client, message)*. This will be the function that gets executed every time a new message arrives and Pyrogram will
    call that function by passing the client instance and the new message instance as argument.

    .. code-block:: python

        def my_function(client, message):
            print(message)

#.  The :class:`~pyrogram.MessageHandler`. This object tells Pyrogram the function we defined above must only handle
    updates that are in form of a :class:`~pyrogram.Message`:

    .. code-block:: python

        my_handler = MessageHandler(my_function)

#.  The method :meth:`~pyrogram.Client.add_handler`. This method is used to actually register the handler and let
    Pyrogram know it needs to be taken into consideration when new updates arrive and the internal dispatching phase
    begins.

    .. code-block:: python

        app.add_handler(my_handler)

#.  The :meth:`~pyrogram.Client.run` method. What this does is simply call :meth:`~pyrogram.Client.start` and
    a special method :meth:`~pyrogram.Client.idle` that keeps your main scripts alive until you press ``CTRL+C``; the
    client will be automatically stopped after that.

    .. code-block:: python

        app.run()

Using Decorators
----------------

All of the above will become quite verbose, especially in case you have lots of handlers to register. A much nicer way
to do so is by decorating your callback function with the :meth:`~pyrogram.Client.on_message` decorator.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")


    @app.on_message()
    def my_handler(client, message):
        print(message)


    app.run()

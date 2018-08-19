Update Handling
===============

Updates are events that happen in your Telegram account (incoming messages, new channel posts, new members join, ...)
and can be handled by registering one or more callback functions in your app by using an `Handler <../pyrogram/Handlers.html>`_.

To put it simply, whenever an update is received from Telegram it will be dispatched and your previously defined callback
function(s) will be called back with the update itself as argument.

Registering an Handler
----------------------

To explain how `Handlers <../pyrogram/Handlers.html>`_ work let's have a look at the most used one, the
:obj:`MessageHandler <pyrogram.MessageHandler>`, which will be in charge for handling :obj:`Message <pyrogram.Message>`
updates coming from all around your chats. Every other handler shares the same setup logic; you should not have troubles
settings them up once you learn from this section.


Using Decorators
----------------

The easiest and nicest way to register a MessageHandler is by decorating your function with the
:meth:`on_message() <pyrogram.Client.on_message>` decorator. Here's a full example that prints out the content
of a message as soon as it arrives.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")


    @app.on_message()
    def my_handler(client, message):
        print(message)


    app.run()

Using add_handler()
-------------------

If you prefer not to use decorators for any reason, there is an alternative way for registering Handlers.
This is useful, for example, when you want to keep your callback functions in separate files.

.. code-block:: python

    from pyrogram import Client, MessageHandler


    def my_handler(client, message):
        print(message)


    app = Client("my_account")

    app.add_handler(MessageHandler(my_handler))

    app.run()

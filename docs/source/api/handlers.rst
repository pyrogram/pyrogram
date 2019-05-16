Update Handlers
===============

Handlers are used to instruct Pyrogram about which kind of updates you'd like to handle with your callback functions.

For a much more convenient way of registering callback functions have a look at `Decorators <Decorators.html>`_ instead.
In case you decided to manually create an handler, use :meth:`add_handler() <pyrogram.Client.add_handler>` to register
it.

.. code-block:: python
    :emphasize-lines: 1, 10

    from pyrogram import Client, MessageHandler

    app = Client("my_account")


    def dump(client, message):
        print(message)


    app.add_handler(MessageHandler(dump))

    app.run()

.. currentmodule:: pyrogram

.. autosummary::
    :nosignatures:

    MessageHandler
    DeletedMessagesHandler
    CallbackQueryHandler
    InlineQueryHandler
    UserStatusHandler
    PollHandler
    DisconnectHandler
    RawUpdateHandler

.. autoclass:: MessageHandler()
    :members:

.. autoclass:: DeletedMessagesHandler()
    :members:

.. autoclass:: CallbackQueryHandler()
    :members:

.. autoclass:: InlineQueryHandler()
    :members:

.. autoclass:: UserStatusHandler()
    :members:

.. autoclass:: PollHandler()
    :members:

.. autoclass:: DisconnectHandler()
    :members:

.. autoclass:: RawUpdateHandler()
    :members:


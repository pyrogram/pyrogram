Update Handlers
===============

Handlers are used to instruct Pyrogram about which kind of updates you'd like to handle with your callback functions.

For a much more convenient way of registering callback functions have a look at :doc:`Decorators <decorators>` instead.
In case you decided to manually create a handler, use :class:`~pyrogram.Client.add_handler` to register
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

Index
-----

.. hlist::
    :columns: 3

    - :class:`MessageHandler`
    - :class:`DeletedMessagesHandler`
    - :class:`CallbackQueryHandler`
    - :class:`InlineQueryHandler`
    - :class:`UserStatusHandler`
    - :class:`PollHandler`
    - :class:`DisconnectHandler`
    - :class:`RawUpdateHandler`

-----

Details
-------

.. Handlers
.. autoclass:: MessageHandler()
.. autoclass:: DeletedMessagesHandler()
.. autoclass:: CallbackQueryHandler()
.. autoclass:: InlineQueryHandler()
.. autoclass:: UserStatusHandler()
.. autoclass:: PollHandler()
.. autoclass:: DisconnectHandler()
.. autoclass:: RawUpdateHandler()

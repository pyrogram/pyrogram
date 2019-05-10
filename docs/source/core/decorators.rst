Decorators
==========

While still being methods bound to the :obj:`Client` class, decorators are of a special kind and thus deserve a
dedicated page.

Decorators are able to register callback functions for handling updates in a much easier and cleaner way compared to
`Handlers <Handlers.html>`_; they do so by instantiating the correct handler and calling
:meth:`add_handler() <pyrogram.Client.add_handler>`, automatically. All you need to do is adding the decorators on top
of your functions.

**Example:**

.. code-block:: python

    from pyrogram import Client

    app = Client(...)


    @app.on_message()
    def log(client, message):
        print(message)


    app.run()

.. currentmodule:: pyrogram.Client

.. autosummary::
    :nosignatures:

    on_message
    on_callback_query
    on_inline_query
    on_deleted_messages
    on_user_status
    on_disconnect
    on_raw_update

.. automethod:: pyrogram.Client.on_message()
.. automethod:: pyrogram.Client.on_callback_query()
.. automethod:: pyrogram.Client.on_inline_query()
.. automethod:: pyrogram.Client.on_deleted_messages()
.. automethod:: pyrogram.Client.on_user_status()
.. automethod:: pyrogram.Client.on_disconnect()
.. automethod:: pyrogram.Client.on_raw_update()
Why is the event handler called twice or more?
==============================================

The event handler is being called twice or more because one or more message edit events have arrived.
By default, Pyrogram listens to both new and edit message events inside ``on_message`` handlers. To prevent edit events
from calling the handler, use the "not edited" filter ``~filters.edited``.

For example:

.. code-block:: python

    ...

    @app.on_message(... & ~filters.edited)
    async def handler(client, message):
        ...

Or, avoid handling any edited message altogether this way:

.. code-block:: python

    ...

    @app.on_message(filters.edited)
    async def edited(client, message):
        pass

    ...  # other handlers
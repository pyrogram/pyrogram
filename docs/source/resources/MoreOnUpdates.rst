More on Updates
===============

Here we'll show some advanced usages when working with updates.

.. note::
    This page makes use of Handlers and Filters to show you how to handle updates.
    Learn more at `Update Handling <UpdateHandling.html>`_ and `Using Filters <UsingFilters.html>`_.

Handler Groups
--------------

If you register handlers with overlapping filters, only the first one is executed and any other handler will be ignored.

In order to process the same update more than once, you can register your handler in a different group.
Groups are identified by a number (number 0 being the default) and are sorted, that is, a lower group number has a
higher priority.

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

Or, if you want ``just_text`` to be fired *before* ``text_or_sticker`` (note ``-1``, which is less than ``0``):

.. code-block:: python

    @app.on_message(Filters.text, group=-1)
    def just_text(client, message):
        print("Just Text")

With :meth:`add_handler() <pyrogram.Client.add_handler>` (without decorators) the same can be achieved with:

.. code-block:: python

    app.add_handler(MessageHandler(just_text, Filters.text), -1)

Update propagation
------------------

Registering multiple handlers, each in a different group, becomes useful when you want to handle the same update more
than once. Any incoming update will be sequentially processed by all of your registered functions by respecting the
groups priority policy described above. Even in case any handler raises an unhandled exception, Pyrogram will still
continue to propagate the same update to the next groups until all the handlers are done. Example:

.. code-block:: python

    @app.on_message(Filters.private)
    def _(client, message):
        print(0)


    @app.on_message(Filters.private, group=1)
    def _(client, message):
        print(1 / 0)  # Unhandled exception: ZeroDivisionError


    @app.on_message(Filters.private, group=2)
    def _(client, message):
        print(2)

All these handlers will handle the same kind of messages, that are, messages sent or received in private chats.
The output for each incoming update will therefore be:

.. code-block:: text

    0
    ZeroDivisionError: division by zero
    2

Stop Propagation
^^^^^^^^^^^^^^^^

In order to prevent further propagation of an update in the dispatching phase, you can do *one* of the following:

- Call the update's bound-method ``.stop_propagation()`` (preferred way).
- Manually ``raise StopPropagation`` error (more suitable for raw updates only).

.. note::

    Note that ``.stop_propagation()`` is just an elegant and intuitive way to raise a ``StopPropagation`` error;
    this means that any code coming *after* calling it won't be executed as your function just raised a custom exception
    to signal the dispatcher not to propagate the update anymore.

Example with ``stop_propagation()``:

.. code-block:: python

    @app.on_message(Filters.private)
    def _(client, message):
        print(0)


    @app.on_message(Filters.private, group=1)
    def _(client, message):
        print(1)
        message.stop_propagation()


    @app.on_message(Filters.private, group=2)
    def _(client, message):
        print(2)

Example with ``raise StopPropagation``:

.. code-block:: python

    from pyrogram import StopPropagation

    @app.on_message(Filters.private)
    def _(client, message):
        print(0)


    @app.on_message(Filters.private, group=1)
    def _(client, message):
        print(1)
        raise StopPropagation


    @app.on_message(Filters.private, group=2)
    def _(client, message):
        print(2)

The handler in group number 2 will never be executed because the propagation was stopped before. The output of both
examples will be:

.. code-block:: text

    0
    1

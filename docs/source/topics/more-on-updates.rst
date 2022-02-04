More on Updates
===============

Here we'll show some advanced usages when working with :doc:`update handlers <../start/updates>` and
:doc:`filters <use-filters>`.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Handler Groups
--------------

If you register handlers with overlapping (conflicting) filters, only the first one is executed and any other handler
will be ignored. This is intended by design.

In order to handle the very same update more than once, you have to register your handler in a different dispatching
group. Dispatching groups hold one or more handlers and are processed sequentially, they are identified by a number
(number 0 being the default) and sorted, that is, a lower group number has a higher priority:

For example, take these two handlers:

.. code-block:: python

    @app.on_message(filters.text | filters.sticker)
    def text_or_sticker(client, message):
        print("Text or Sticker")


    @app.on_message(filters.text)
    def just_text(client, message):
        print("Just Text")

Here, ``just_text`` is never executed because ``text_or_sticker``, which has been registered first, already handles
texts (``filters.text`` is shared and conflicting). To enable it, register the handler using a different group:

.. code-block:: python

    @app.on_message(filters.text, group=1)
    def just_text(client, message):
        print("Just Text")

Or, if you want ``just_text`` to be executed *before* ``text_or_sticker`` (note ``-1``, which is less than ``0``):

.. code-block:: python

    @app.on_message(filters.text, group=-1)
    def just_text(client, message):
        print("Just Text")

With :meth:`~pyrogram.Client.add_handler` (without decorators) the same can be achieved with:

.. code-block:: python

    app.add_handler(MessageHandler(just_text, filters.text), -1)

Update propagation
------------------

Registering multiple handlers, each in a different group, becomes useful when you want to handle the same update more
than once. Any incoming update will be sequentially processed by all of your registered functions by respecting the
groups priority policy described above. Even in case any handler raises an unhandled exception, Pyrogram will still
continue to propagate the same update to the next groups until all the handlers are done. Example:

.. code-block:: python

    @app.on_message(filters.private)
    def _(client, message):
        print(0)


    @app.on_message(filters.private, group=1)
    def _(client, message):
        raise Exception("Unhandled exception!")  # Simulate an unhandled exception


    @app.on_message(filters.private, group=2)
    def _(client, message):
        print(2)

All these handlers will handle the same kind of messages, that are, messages sent or received in private chats.
The output for each incoming update will therefore be:

.. code-block:: text

    0
    Exception: Unhandled exception!
    2

Stop Propagation
^^^^^^^^^^^^^^^^

In order to prevent further propagation of an update in the dispatching phase, you can do *one* of the following:

- Call the update's bound-method ``.stop_propagation()`` (preferred way).
- Manually ``raise StopPropagation`` exception (more suitable for raw updates only).

.. note::

    Internally, the propagation is stopped by handling a custom exception. ``.stop_propagation()`` is just an elegant
    and intuitive way to ``raise StopPropagation``; this also means that any code coming *after* calling the method
    won't be executed as your function just raised an exception to signal the dispatcher not to propagate the
    update anymore.

Example with ``stop_propagation()``:

.. code-block:: python

    @app.on_message(filters.private)
    def _(client, message):
        print(0)


    @app.on_message(filters.private, group=1)
    def _(client, message):
        print(1)
        message.stop_propagation()


    @app.on_message(filters.private, group=2)
    def _(client, message):
        print(2)

Example with ``raise StopPropagation``:

.. code-block:: python

    from pyrogram import StopPropagation

    @app.on_message(filters.private)
    def _(client, message):
        print(0)


    @app.on_message(filters.private, group=1)
    def _(client, message):
        print(1)
        raise StopPropagation


    @app.on_message(filters.private, group=2)
    def _(client, message):
        print(2)

Each handler is registered in a different group, but the handler in group number 2 will never be executed because the
propagation was stopped earlier. The output of both (equivalent) examples will be:

.. code-block:: text

    0
    1

Continue Propagation
^^^^^^^^^^^^^^^^^^^^

As opposed to `stopping the update propagation <#stop-propagation>`_ and also as an alternative to the
`handler groups <#handler-groups>`_, you can signal the internal dispatcher to continue the update propagation within
**the same group** despite having conflicting filters in the next registered handler. This allows you to register
multiple handlers with overlapping filters in the same group; to let the dispatcher process the next handler you can do
*one* of the following in each handler you want to grant permission to continue:

- Call the update's bound-method ``.continue_propagation()`` (preferred way).
- Manually ``raise ContinuePropagation`` exception (more suitable for raw updates only).

.. note::

    Internally, the propagation is continued by handling a custom exception. ``.continue_propagation()`` is just an
    elegant and intuitive way to ``raise ContinuePropagation``; this also means that any code coming *after* calling the
    method won't be executed as your function just raised an exception to signal the dispatcher to continue with the
    next available handler.


Example with ``continue_propagation()``:

.. code-block:: python

    @app.on_message(filters.private)
    def _(client, message):
        print(0)
        message.continue_propagation()


    @app.on_message(filters.private)
    def _(client, message):
        print(1)
        message.continue_propagation()


    @app.on_message(filters.private)
    def _(client, message):
        print(2)

Example with ``raise ContinuePropagation``:

.. code-block:: python

    from pyrogram import ContinuePropagation

    @app.on_message(filters.private)
    def _(client, message):
        print(0)
        raise ContinuePropagation


    @app.on_message(filters.private)
    def _(client, message):
        print(1)
        raise ContinuePropagation


    @app.on_message(filters.private)
    def _(client, message):
        print(2)

Three handlers are registered in the same group, and all of them will be executed because the propagation was continued
in each handler (except in the last one, where is useless to do so since there is no more handlers after).
The output of both (equivalent) examples will be:

.. code-block:: text

    0
    1
    2

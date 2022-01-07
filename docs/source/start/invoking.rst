Calling Methods
===============

At this point, we have successfully :doc:`installed Pyrogram <../intro/install>` and :doc:`authorized <auth>` our
account; we are now aiming towards the core of the framework.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Basic Usage
-----------

Making API method calls with Pyrogram is very simple. Here's a basic example we are going to examine step by step:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    async def main():
        async with app:
            await app.send_message("me", "Hi!")

    app.run(main())

Step-by-step
^^^^^^^^^^^^

#.  Let's begin by importing the Client class.

    .. code-block:: python

        from pyrogram import Client

#.  Now instantiate a new Client object, "my_account" is a session name of your choice.

    .. code-block:: python

        app = Client("my_account")

#.  Async methods can't be executed at the top level, because they must be inside an async context.
    Here we define an async function and put our code inside. Also notice the ``await`` keyword in front of the method
    call; this is required for all asynchronous methods.

    .. code-block:: python

        async def main():
            async with app:
                await app.send_message("me", "Hi!")

#.  Finally, we tell Python to schedule our ``main()`` async function by using Pyrogram's :meth:`~pyrogram.Client.run`
    method.

    .. code-block:: python

        app.run(main())

Context Manager
---------------

The ``async with`` statement starts a context manager, which is used as a shortcut for starting, executing and stopping
the Client, asynchronously. It does so by automatically calling :meth:`~pyrogram.Client.start` and
:meth:`~pyrogram.Client.stop` in a more convenient way which also gracefully stops the client, even in case of
unhandled exceptions in your code.

Below there's the same example as above, but without the use of the context manager:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    async def main():
        await app.start()
        await app.send_message("me", "Hi!")
        await app.stop()

    app.run(main())

Using asyncio.run()
-------------------

Alternatively to the :meth:`~pyrogram.Client.run` method, you can use Python's ``asyncio.run()`` to execute the main
function, with one little caveat: the Client instance (and possibly other asyncio resources you are going to use) must
be instantiated inside the main function.

.. code-block:: python

    import asyncio
    from pyrogram import Client

    async def main():
        app = Client("my_account")

        async with app:
            await app.send_message("me", "Hi!")

    asyncio.run(main())

Synchronous Calls
------------------

Pyrogram is an asynchronous framework, but it also provides a convenience way for calling methods without the need
of async/await keywords and the extra boilerplate. In case you want Pyrogram to run synchronously, simply  use the
synchronous context manager:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    with app:
        app.send_message("me", "Hi!")

As you can see, the non-async example becomes less cluttered. Use Pyrogram in this non-asynchronous way only when you
want to write something without the boilerplate or in case you want to combine Pyrogram with other libraries that are
not async.
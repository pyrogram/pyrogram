Calling Methods
===============

At this point, we have successfully :doc:`installed Pyrogram <../intro/install>` and :doc:`authorized <auth>` our
account; we are now aiming towards the core of the library. It's time to start playing with the API!

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Basic Usage
-----------

Making API method calls with Pyrogram is very simple. Here's a basic example we are going to examine step by step and
then expand to explain what happens underneath:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    with app:
        app.send_message("me", "Hi!")

Basic step-by-step
^^^^^^^^^^^^^^^^^^

#.  Let's begin by importing the Client class:

    .. code-block:: python

        from pyrogram import Client

#.  Now instantiate a new Client object, "my_account" is a session name of your choice:

    .. code-block:: python

        app = Client("my_account")

#.  The ``with`` context manager is a shortcut for starting, executing and stopping the Client:

    .. code-block:: python

        with app:

#.  Now, you can call any method you like:

    .. code-block:: python

        app.send_message("me", "Hi!")

Context Manager
---------------

The ``with`` statement starts a context manager, which is used as a shortcut to automatically call
:meth:`~pyrogram.Client.start` and :meth:`~pyrogram.Client.stop`, which are methods required for Pyrogram to work
properly. The context manager does also gracefully stop the client, even in case of unhandled exceptions in your code.

This is how Pyrogram looks without the context manager:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    app.start()
    app.send_message("me", "Hi!")
    app.stop()

Asynchronous Calls
------------------

In case you want Pyrogram to run asynchronously (e.g.: if you are using third party libraries that require you to call
them with ``await``), use the asynchronous context manager:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    async def main():
        async with app:
            await app.send_message("me", "Hi!")

    app.run(main())

Asynchronous step-by-step
^^^^^^^^^^^^^^^^^^^^^^^^^

#.  Import the Client class and create an instance:

    .. code-block:: python

        from pyrogram import Client

        app = Client("my_account")

#.  Async methods can't normally be executed at the top level, because they must be inside an async-defined function;
    here we define one and put our code inside; the context manager is also being used differently in asyncio and
    method calls require the await keyword:

    .. code-block:: python

        async def main():
            async with app:
                await app.send_message("me", "Hi!")

#.  Finally, we tell Python to schedule our ``main()`` async function, which in turn will execute Pyrogram's code. Using
    :meth:`~pyrogram.Client.run` this way is a friendly alternative for the much more verbose
    ``asyncio.get_event_loop().run_until_complete(main())``:

    .. code-block:: python

        app.run(main())

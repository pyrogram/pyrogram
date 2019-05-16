Calling Methods
===============

At this point, we have successfully `installed Pyrogram`_ and authorized_ our account; we are now aiming towards the
core of the library. It's time to start playing with the API!

Basic Usage
-----------

Making API method calls with Pyrogram is very simple. Here's an example we are going to examine:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    app.start()

    print(app.get_me())
    app.send_message("me", "Hi, it's me!")
    app.send_location("me", 51.500729, -0.124583)
    app.send_sticker("me", "CAADBAADyg4AAvLQYAEYD4F7vcZ43AI")

    app.stop()

Let's begin by importing the Client class from the Pyrogram package:

.. code-block:: python

    from pyrogram import Client

Now instantiate a new Client object, "my_account" is a session name of your choice:

.. code-block:: python

    app = Client("my_account")

To actually make use of any method, the client has to be started:

.. code-block:: python

    app.start()

Now, you can call any method you like:

.. code-block:: python

    print(app.get_me())  # Print information about yourself

    # Send messages to yourself:
    app.send_message("me", "Hi!")  # Text message
    app.send_location("me", 51.500729, -0.124583)  # Location
    app.send_sticker("me", "CAADBAADyg4AAvLQYAEYD4F7vcZ43AI")  # Sticker

Finally, when done, simply stop the client:

.. code-block:: python

    app.stop()

Context Manager
---------------

You can also use Pyrogram's Client in a context manager with the ``with`` statement. The client will automatically
:meth:`start() <pyrogram.Client.start>` and :meth:`stop() <pyrogram.Client.stop>` gracefully, even in case of unhandled
exceptions in your code. The example above can be therefore rewritten in a much nicer way:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    with app:
        print(app.get_me())
        app.send_message("me", "Hi there! I'm using **Pyrogram**")
        app.send_location("me", 51.500729, -0.124583)
        app.send_sticker("me", "CAADBAADyg4AAvLQYAEYD4F7vcZ43AI")

More examples can be found on `GitHub <https://github.com/pyrogram/pyrogram/tree/develop/examples>`_.

.. _installed Pyrogram: ../intro/install.html
.. _authorized: ../intro/setup.html

Smart Plugins
=============

Pyrogram embeds a **smart** (automatic) and lightweight plugin system that is meant to further simplify the organization
of large projects and to provide a way for creating pluggable components that can be **easily shared** across different
Pyrogram applications with **minimal boilerplate code**.

Introduction
------------

Prior to the Smart Plugin system, pluggable handlers were already possible. For example, if you wanted to modularize
your applications, you had to do something like this...

.. note:: This is an example application that replies in private chats with two messages: one containing the same
    text message you sent and the other containing the reversed text message (e.g.: "pyrogram" -> "pyrogram" and
    "margoryp"):

.. code-block:: text

    myproject/
        config.ini
        handlers.py
        main.py

- ``handlers.py``

    .. code-block:: python

        def echo(client, message):
            message.reply(message.text)


        def echo_reversed(client, message):
            message.reply(message.text[::-1])

- ``main.py``

    .. code-block:: python

        from pyrogram import Client, MessageHandler, Filters

        from handlers import echo, echo_reversed

        app = Client("my_account")

        app.add_handler(
            MessageHandler(
                echo,
                Filters.text & Filters.private))

        app.add_handler(
            MessageHandler(
                echo_reversed,
                Filters.text & Filters.private),
            group=1)

        app.run()

...which is already nice and doesn't add *too much* boilerplate code, but things can get boring still; you have to
manually ``import``, manually :meth:`add_handler <pyrogram.Client.add_handler>` and manually instantiate each
:obj:`MessageHandler <pyrogram.MessageHandler>` object because **you can't use those cool decorators** for your
functions. So... What if you could?

Using Smart Plugins
-------------------

Setting up your Pyrogram project to accommodate Smart Plugins is pretty straightforward:

#. Create a new folder to store all the plugins (e.g.: "plugins").
#. Put your files full of plugins inside.
#. Enable plugins in your Client.

.. note::

    This is the same example application `as shown above <#introduction>`_, written using the Smart Plugin system.

.. code-block:: text
    :emphasize-lines: 2, 3

    myproject/
        plugins/
            handlers.py
        config.ini
        main.py

- ``plugins/handlers.py``

    .. code-block:: python
        :emphasize-lines: 4, 9

        from pyrogram import Client, Filters


        @Client.on_message(Filters.text & Filters.private)
        def echo(client, message):
            message.reply(message.text)


        @Client.on_message(Filters.text & Filters.private, group=1)
        def echo_reversed(client, message):
            message.reply(message.text[::-1])

- ``main.py``

    .. code-block:: python

        from pyrogram import Client

        Client("my_account", plugins_dir="plugins").run()

The first important thing to note is the new ``plugins`` folder, whose name is passed to the the ``plugins_dir``
parameter when creating a :obj:`Client <pyrogram.Client>` in the ``main.py`` file — you can put *any python file* in
there and each file can contain *any decorated function* (handlers) with only one limitation: within a single plugin
file you must use different names for each decorated function. Your Pyrogram Client instance will **automatically**
scan the folder upon creation to search for valid handlers and register them for you.

Then you'll notice you can now use decorators. That's right, you can apply the usual decorators to your callback
functions in a static way, i.e. **without having the Client instance around**: simply use ``@Client`` (Client class)
instead of the usual ``@app`` (Client instance) namespace and things will work just the same.

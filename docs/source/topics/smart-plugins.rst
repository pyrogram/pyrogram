Smart Plugins
=============

Pyrogram embeds a smart, lightweight yet powerful plugin system that is meant to further simplify the organization
of large projects and to provide a way for creating pluggable (modular) components that can be easily shared across
different Pyrogram applications with minimal boilerplate code.

.. tip::

    Smart Plugins are completely optional and disabled by default.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Introduction
------------

Prior to the Smart Plugin system, pluggable handlers were already possible. For example, if you wanted to modularize
your applications, you had to put your function definitions in separate files and register them inside your main script
after importing your modules, like this:

.. note::

    This is an example application that replies in private chats with two messages: one containing the same
    text message you sent and the other containing the reversed text message.

    Example: *"Pyrogram"* replies with *"Pyrogram"* and *"margoryP"*

.. code-block:: text

    myproject/
        config.ini
        handlers.py
        main.py

-   ``handlers.py``

    .. code-block:: python

        def echo(client, message):
            message.reply(message.text)


        def echo_reversed(client, message):
            message.reply(message.text[::-1])

-   ``main.py``

    .. code-block:: python

        from pyrogram import Client, filters
        from pyrogram.handlers import MessageHandler

        from handlers import echo, echo_reversed

        app = Client("my_account")

        app.add_handler(
            MessageHandler(
                echo,
                filters.text & filters.private))

        app.add_handler(
            MessageHandler(
                echo_reversed,
                filters.text & filters.private),
            group=1)

        app.run()

This is already nice and doesn't add *too much* boilerplate code, but things can get boring still; you have to
manually ``import``, manually :meth:`~pyrogram.Client.add_handler` and manually instantiate each
:class:`~pyrogram.handlers.MessageHandler` object because you can't use decorators for your functions.
So, what if you could? Smart Plugins solve this issue by taking care of handlers registration automatically.

Using Smart Plugins
-------------------

Setting up your Pyrogram project to accommodate Smart Plugins is pretty straightforward:

#. Create a new folder to store all the plugins (e.g.: "plugins", "handlers", ...).
#. Put your python files full of plugins inside. Organize them as you wish.
#. Enable plugins in your Client or via the *config.ini* file.

.. note::

    This is the same example application as shown above, written using the Smart Plugin system.

.. code-block:: text

    myproject/
        plugins/
            handlers.py
        config.ini
        main.py

-   ``plugins/handlers.py``

    .. code-block:: python

        from pyrogram import Client, filters


        @Client.on_message(filters.text & filters.private)
        def echo(client, message):
            message.reply(message.text)


        @Client.on_message(filters.text & filters.private, group=1)
        def echo_reversed(client, message):
            message.reply(message.text[::-1])

-   ``config.ini``

    .. code-block:: ini

        [plugins]
        root = plugins

-   ``main.py``

    .. code-block:: python

        from pyrogram import Client

        Client("my_account").run()

    Alternatively, without using the *config.ini* file:

    .. code-block:: python

        from pyrogram import Client

        plugins = dict(root="plugins")

        Client("my_account", plugins=plugins).run()


The first important thing to note is the new ``plugins`` folder. You can put *any python file* in *any subfolder* and
each file can contain *any decorated function* (handlers) with one limitation: within a single module (file) you must
use different names for each decorated function.

The second thing is telling Pyrogram where to look for your plugins: you can either use the *config.ini* file or
the Client parameter "plugins"; the *root* value must match the name of your plugins root folder. Your Pyrogram Client
instance will **automatically** scan the folder upon starting to search for valid handlers and register them for you.

Then you'll notice you can now use decorators. That's right, you can apply the usual decorators to your callback
functions in a static way, i.e. **without having the Client instance around**: simply use ``@Client`` (Client class)
instead of the usual ``@app`` (Client instance) and things will work just the same.

Specifying the Plugins to include
---------------------------------

By default, if you don't explicitly supply a list of plugins, every valid one found inside your plugins root folder will
be included by following the alphabetical order of the directory structure (files and subfolders); the single handlers
found inside each module will be, instead, loaded in the order they are defined, from top to bottom.

.. note::

    Remember: there can be at most one handler, within a group, dealing with a specific update. Plugins with overlapping
    filters included a second time will not work, by design. Learn more at :doc:`More on Updates <more-on-updates>`.

This default loading behaviour is usually enough, but sometimes you want to have more control on what to include (or
exclude) and in which exact order to load plugins. The way to do this is to make use of ``include`` and ``exclude``
directives, either in the *config.ini* file or in the dictionary passed as Client argument. Here's how they work:

- If both ``include`` and ``exclude`` are omitted, all plugins are loaded as described above.
- If ``include`` is given, only the specified plugins will be loaded, in the order they are passed.
- If ``exclude`` is given, the plugins specified here will be unloaded.

The ``include`` and ``exclude`` value is a **list of strings**. Each string containing the path of the module relative
to the plugins root folder, in Python notation (dots instead of slashes).

    E.g.: ``subfolder.module`` refers to ``plugins/subfolder/module.py``, with ``root="plugins"``.

You can also choose the order in which the single handlers inside a module are loaded, thus overriding the default
top-to-bottom loading policy. You can do this by appending the name of the functions to the module path, each one
separated by a blank space.

    E.g.: ``subfolder.module fn2 fn1 fn3`` will load *fn2*, *fn1* and *fn3* from *subfolder.module*, in this order.

Examples
^^^^^^^^

Given this plugins folder structure with three modules, each containing their own handlers (fn1, fn2, etc...), which are
also organized in subfolders:

.. code-block:: text

    myproject/
        plugins/
            subfolder1/
                plugins1.py
                    - fn1
                    - fn2
                    - fn3
            subfolder2/
                plugins2.py
                    ...
            plugins0.py
                ...
        ...

-   Load every handler from every module, namely *plugins0.py*, *plugins1.py* and *plugins2.py* in alphabetical order
    (files) and definition order (handlers inside files):

    Using *config.ini* file:

    .. code-block:: ini

        [plugins]
        root = plugins

    Using *Client*'s parameter:

    .. code-block:: python

        plugins = dict(root="plugins")

        Client("my_account", plugins=plugins).run()

-   Load only handlers defined inside *plugins2.py* and *plugins0.py*, in this order:

    Using *config.ini* file:

    .. code-block:: ini

        [plugins]
        root = plugins
        include =
            subfolder2.plugins2
            plugins0

    Using *Client*'s parameter:

    .. code-block:: python

        plugins = dict(
            root="plugins",
            include=[
                "subfolder2.plugins2",
                "plugins0"
            ]
        )

        Client("my_account", plugins=plugins).run()

-   Load everything except the handlers inside *plugins2.py*:

    Using *config.ini* file:

    .. code-block:: ini

        [plugins]
        root = plugins
        exclude = subfolder2.plugins2

    Using *Client*'s parameter:

    .. code-block:: python

        plugins = dict(
            root="plugins",
            exclude=["subfolder2.plugins2"]
        )

        Client("my_account", plugins=plugins).run()

-   Load only *fn3*, *fn1* and *fn2* (in this order) from *plugins1.py*:

    Using *config.ini* file:

    .. code-block:: ini

        [plugins]
        root = plugins
        include = subfolder1.plugins1 fn3 fn1 fn2

    Using *Client*'s parameter:

    .. code-block:: python

        plugins = dict(
            root="plugins",
            include=["subfolder1.plugins1 fn3 fn1 fn2"]
        )

        Client("my_account", plugins=plugins).run()

Load/Unload Plugins at Runtime
------------------------------

In the previous section we've explained how to specify which plugins to load and which to ignore before your Client
starts. Here we'll show, instead, how to unload and load again a previously registered plugin at runtime.

Each function decorated with the usual ``on_message`` decorator (or any other decorator that deals with Telegram
updates) will be modified in such a way that a special ``handlers`` attribute pointing to a list of tuples of
*(handler: Handler, group: int)* is attached to the function object itself.

-   ``plugins/handlers.py``

    .. code-block:: python

        @Client.on_message(filters.text & filters.private)
        def echo(client, message):
            message.reply(message.text)

        print(echo)
        print(echo.handlers)

-   Printing ``echo`` will show something like ``<function echo at 0x10e3b6598>``.

-   Printing ``echo.handlers`` will reveal the handlers, that is, a list of tuples containing the actual handlers and
    the groups they were registered on ``[(<MessageHandler object at 0x10e3abc50>, 0)]``.

Unloading
^^^^^^^^^

In order to unload a plugin, all you need to do is obtain a reference to it by importing the relevant module and call
:meth:`~pyrogram.Client.remove_handler` Client's method with your function's *handler* instance:

-   ``main.py``

    .. code-block:: python

        from plugins.handlers import echo

        handlers = echo.handlers

        for h in handlers:
            app.remove_handler(*h)

The star ``*`` operator is used to unpack the tuple into positional arguments so that *remove_handler* will receive
exactly what is needed. The same could have been achieved with:

.. code-block:: python

    handlers = echo.handlers
    handler, group = handlers[0]

    app.remove_handler(handler, group)

Loading
^^^^^^^

Similarly to the unloading process, in order to load again a previously unloaded plugin you do the same, but this time
using :meth:`~pyrogram.Client.add_handler` instead. Example:

-   ``main.py``

    .. code-block:: python

        from plugins.handlers import echo

        ...

        handlers = echo.handlers

        for h in handlers:
            app.add_handler(*h)
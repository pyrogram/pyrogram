Storage Engines
===============

Every time you login to Telegram, some personal piece of data are created and held by both parties (the client, Pyrogram
and the server, Telegram). This session data is uniquely bound to your own account, indefinitely (until you logout or
decide to manually terminate it) and is used to authorize a client to execute API calls on behalf of your identity.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Persisting Sessions
-------------------

In order to make a client reconnect successfully between restarts, that is, without having to start a new
authorization process from scratch each time, Pyrogram needs to store the generated session data somewhere.

Different Storage Engines
-------------------------

Pyrogram offers two different types of storage engines: a **File Storage** and a **Memory Storage**.
These engines are well integrated in the framework and require a minimal effort to set up. Here's how they work:

File Storage
^^^^^^^^^^^^

This is the most common storage engine. It is implemented by using **SQLite**, which will store the session details.
The database will be saved to disk as a single portable file and is designed to efficiently store and retrieve
data whenever they are needed.

To use this type of engine, simply pass any name of your choice to the ``session_name`` parameter of the
:obj:`~pyrogram.Client` constructor, as usual:

.. code-block:: python

    from pyrogram import Client

    with Client("my_account") as app:
        print(app.get_me())

Once you successfully log in (either with a user or a bot identity), a session file will be created and saved to disk as
``my_account.session``. Any subsequent client restart will make Pyrogram search for a file named that way and the
session database will be automatically loaded.

Memory Storage
^^^^^^^^^^^^^^

In case you don't want to have any session file saved to disk, you can use an in-memory storage by passing the special
session name "**:memory:**" to the ``session_name`` parameter of the :obj:`~pyrogram.Client` constructor:

.. code-block:: python

    from pyrogram import Client

    with Client(":memory:") as app:
        print(app.get_me())

This storage engine is still backed by SQLite, but the database exists purely in memory. This means that, once you stop
a client, the entire database is discarded and the session details used for logging in again will be lost forever.

Session Strings
---------------

In case you want to use an in-memory storage, but also want to keep access to the session you created, call
:meth:`~pyrogram.Client.export_session_string` anytime before stopping the client...

.. code-block:: python

    from pyrogram import Client

    with Client(":memory:") as app:
        print(app.export_session_string())

...and save the resulting string. You can use this string as session name the next time you want to login
using the same session; the storage used will still be in-memory:

.. code-block:: python

    from pyrogram import Client

    session_string = "...ZnUIFD8jsjXTb8g_vpxx48k1zkov9sapD-tzjz-S4WZv70M..."

    with Client(session_string) as app:
        print(app.get_me())

Session strings are useful when you want to run authorized Pyrogram clients on platforms where their ephemeral
filesystems makes it harder for a file-based storage engine to properly work as intended.

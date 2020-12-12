Storage Engines
===============

Every time you login to Telegram, some personal piece of data are created and held by both parties (the client, Pyrogram
and the server, Telegram). This session data is uniquely bound to your own account, indefinitely (until you logout or
decide to manually terminate it) and is used to authorize a client to execute API calls on behalf of your identity.

.. contents:: Contents
    :backlinks: none
    :local:

-----

Persisting Sessions
-------------------

In order to make a client reconnect successfully between restarts, that is, without having to start a new
authorization process from scratch each time, Pyrogram needs to store the generated session data somewhere.

Other useful data being stored is peers' cache. In short, peers are all those entities you can chat with, such as users
or bots, basic groups, but also channels and supergroups. Because of how Telegram works, a unique pair of **id** and
**access_hash** is needed to contact a peer. This, plus other useful info such as the peer type, is what is stored
inside a session storage.

So, if you ever wondered how is Pyrogram able to contact peers just by asking for their ids, it's because of this very
reason: the peer *id* is looked up in the internal database and the available *access_hash* is retrieved, which is then
used to correctly invoke API methods.

Different Storage Engines
-------------------------

Let's now talk about how Pyrogram actually stores all the relevant data. Pyrogram offers two different types of storage
engines: a **File Storage** and a **Memory Storage**. These engines are well integrated in the library and require a
minimal effort to set up. Here's how they work:

File Storage
^^^^^^^^^^^^

This is the most common storage engine. It is implemented by using **SQLite**, which will store the session and peers
details. The database will be saved to disk as a single portable file and is designed to efficiently store and retrieve
peers whenever they are needed.

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

This storage engine is still backed by SQLite, but the database exists purely in memory. This means that, once you stop a
client, the entire database is discarded and the session details used for logging in again will be lost forever.

Session Strings
---------------

In case you want to use an in-memory storage, but also want to keep access to the session you created, call
:meth:`~pyrogram.Client.export_session_string` anytime before stopping the client...

.. code-block:: python

    from pyrogram import Client

    with Client(":memory:") as app:
        print(app.export_session_string())

...and save the resulting (quite long) string somewhere. You can use this string as session name the next time you want
to login using the same session; the storage used will still be completely in-memory:

.. code-block:: python

    from pyrogram import Client

    session_string = "...ZnUIFD8jsjXTb8g_vpxx48k1zkov9sapD-tzjz-S4WZv70M..."

    with Client(session_string) as app:
        print(app.get_me())

Session strings are useful when you want to run authorized Pyrogram clients on platforms like
`Heroku <https://www.heroku.com/>`_, where their ephemeral filesystems makes it much harder for a file-based storage
engine to properly work as intended.

But, why is the session string so long? Can't it be shorter? No, it can't. The session string already packs the bare
minimum data Pyrogram needs to successfully reconnect to an authorized session, and the 2048-bits auth key is the major
contributor to the overall length. Needless to say that this string, as well as any other session storage, represent
strictly personal data. Keep them safe.

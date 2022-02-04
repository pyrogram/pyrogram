Authorization
=============

Once a :doc:`project is set up <../intro/setup>`, you will still have to follow a few steps before you can actually use Pyrogram to make
API calls. This section provides all the information you need in order to authorize yourself as user or bot.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

User Authorization
------------------

In order to use the API, Telegram requires that users be authorized via their phone numbers.
Pyrogram automatically manages this process, all you need to do is create an instance of the
:class:`~pyrogram.Client` class by passing to it a ``session_name`` of your choice (e.g.: "my_account") and call
the :meth:`~pyrogram.Client.run` method:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")
    app.run()

This starts an interactive shell asking you to input your **phone number**, including your `Country Code`_ (the plus
``+`` and minus ``-`` symbols can be omitted) and the **phone code** you will receive in your devices that are already
authorized or via SMS:

.. code-block:: text

    Enter phone number: +1-123-456-7890
    Is "+1-123-456-7890" correct? (y/n): y
    Enter phone code: 12345
    Logged in successfully

After successfully authorizing yourself, a new file called ``my_account.session`` will be created allowing Pyrogram to
execute API calls with your identity. This file is personal and will be loaded again when you restart your app, and as
long as you keep the session alive, Pyrogram won't ask you again to enter your phone number.

.. note::

    The code above does nothing except asking for credentials and keeping the client online, hit :guilabel:`CTRL+C` now
    to stop your application and keep reading.

Bot Authorization
-----------------

Bots are a special kind of users that are authorized via their tokens (instead of phone numbers), which are created by
the `Bot Father`_. Bot tokens replace the users' phone numbers only — you still need to
:doc:`configure a Telegram API key <../intro/setup>` with Pyrogram, even when using bots.

The authorization process is automatically managed. All you need to do is choose a ``session_name`` (can be anything,
usually your bot username) and pass your bot token using the ``bot_token`` parameter. The session file will be named
after the session name, which will be ``my_bot.session`` for the example below.

.. code-block:: python

    from pyrogram import Client

    app = Client(
        "my_bot",
        bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11"
    )

    app.run()

.. _Country Code: https://en.wikipedia.org/wiki/List_of_country_calling_codes
.. _Bot Father: https://t.me/botfather
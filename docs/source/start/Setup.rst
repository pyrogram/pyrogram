Setup
=====

Once you successfully `installed Pyrogram`_, you will still have to follow a few steps before you can actually use
the library to make API calls. This section provides all the information you need in order to set up a project
with Pyrogram.

API Keys
--------

The very first step requires you to obtain a valid Telegram API key (API id/hash pair).
If you already have one you can skip this step, otherwise:

#. Visit https://my.telegram.org/apps and log in with your Telegram Account.
#. Fill out the form to register a new Telegram application.
#. Done. The API key consists of two parts: **App api_id** and **App api_hash**.


.. important::

     This API key is personal and should be kept secret.

Configuration
-------------

The API key obtained in the `previous step <#api-keys>`_ defines a token for your application allowing you to access
the Telegram database using the MTProto API — **it is therefore required for all authorizations of both Users and Bots**.

Having it handy, it's time to configure your Pyrogram project. There are two ways to do so, and you can choose what
fits better for you:

-   Create a new ``config.ini`` file at the root of your working directory, copy-paste the following and replace the
    **api_id** and **api_hash** values with your own. This is the preferred method because allows you
    to keep your credentials out of your code without having to deal with how to load them:

    .. code-block:: ini

        [pyrogram]
        api_id = 12345
        api_hash = 0123456789abcdef0123456789abcdef

-   Alternatively, you can pass your API key to Pyrogram by simply using the *api_id* and *api_hash*
    parameters of the Client class. This way you can have full control on how to store and load your credentials:

    .. code-block:: python

        from pyrogram import Client

        app = Client(
            "my_account",
            api_id=12345,
            api_hash="0123456789abcdef0123456789abcdef"
        )

.. note::

    The examples below assume you have created a ``config.ini`` file, thus they won't show the *api_id*
    and *api_hash* parameters usage.

User Authorization
------------------

In order to use the API, Telegram requires that Users be authorized via their phone numbers.
Pyrogram automatically manages this access, all you need to do is create an instance of
the :class:`Client <pyrogram.Client>` class by passing to it a ``session_name`` of your choice
(e.g.: "my_account") and call the :meth:`run() <pyrogram.Client.run>` method:

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")
    app.run()

This starts an interactive shell asking you to input your **phone number** (including your `Country Code`_)
and the **phone code** you will receive:

.. code-block:: text

    Enter phone number: +39**********
    Is "+39**********" correct? (y/n): y
    Enter phone code: 32768

After successfully authorizing yourself, a new file called ``my_account.session`` will be created allowing
Pyrogram executing API calls with your identity. This file will be loaded again when you restart your app,
and as long as you keep the session alive, Pyrogram won't ask you again to enter your phone number.

.. important::

    Your ``*.session`` files are personal and must be kept secret.

Bot Authorization
-----------------

Bots are a special kind of users that are authorized via their tokens (instead of phone numbers), which are created by
BotFather_. Bot tokens replace the Users' phone numbers only — you still need to
`configure a Telegram API key <#configuration>`_ with Pyrogram, even when using Bots.

The authorization process is automatically managed. All you need to do is choose a ``session_name`` (can be anything,
usually your bot username) and pass your bot token using the ``bot_token`` parameter.
The session file will be named after the session name, which will be ``pyrogrambot.session`` for the example below.

.. code-block:: python

    from pyrogram import Client

    app = Client("pyrogrambot", bot_token="123456:ABC-DEF1234ghIkl-zyx57W2v1u123ew11")
    app.run()

.. _installed Pyrogram: Installation.html
.. _`Country Code`: https://en.wikipedia.org/wiki/List_of_country_calling_codes
.. _BotFather: https://t.me/botfather
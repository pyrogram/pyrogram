Session Settings
================

As you may probably know, Telegram allows users (and bots) having more than one session (authorizations) registered
in the system at the same time.

Briefly explaining, sessions are simply new logins in your account. They can be reviewed in the settings of an official
app (or by invoking `GetAuthorizations <../telegram/functions/account/GetAuthorizations.html>`_ with Pyrogram). They
store some useful information such as the client who's using them and from which country and IP address.

.. figure:: https://i.imgur.com/YaqtMLO.png
    :width: 600
    :align: center

    **A Pyrogram session running on Linux, Python 3.7.**

That's how a session looks like on the Android app, showing the three main pieces of information.

-   ``app_version``: **Pyrogram 0.13.0**
-   ``device_model``: **CPython 3.7.2**
-   ``system_version``: **Linux 4.15.0-23-generic**

Set Custom Values
-----------------

To set custom values, you can either make use of the ``config.ini`` file, this way:

.. code-block:: ini

    [pyrogram]
    app_version = 1.2.3
    device_model = PC
    system_version = Linux

Or, pass the arguments directly in the Client's constructor.

.. code-block:: python

    app = Client(
        "my_account",
        app_version="1.2.3",
        device_model="PC",
        system_version="Linux"
    )

Set Custom Languages
--------------------

To tell Telegram in which language should speak to you (terms of service, bots, service messages, ...) you can
set ``lang_code`` in `ISO 639-1 <https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes>`_ standard (defaults to "en",
English).

With the following code we make Telegram know we want it to speak in Italian (it):

.. code-block:: ini

    [pyrogram]
    lang_code = it

.. code-block:: python

    app = Client(
        "my_account",
        lang_code="it",
    )
Client Settings
===============

You can control the way your client appears in the Active Sessions menu of an official client by changing some client
settings. By default you will see something like the following:

-   Device Model: ``CPython x.y.z``
-   Application: ``Pyrogram x.y.z``
-   System Version: ``Linux x.y.z``

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

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
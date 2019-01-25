Configuration File
==================

As already mentioned in previous sections, Pyrogram can also be configured by the use of an INI file.
This page explains how this file is structured in Pyrogram, how to use it and why.

Introduction
------------

The idea behind using a configuration file is to help keeping your code free of settings (private) information such as
the API Key and Proxy without having you to even deal with how to load such settings. The configuration file, usually
referred as ``config.ini` file, is automatically loaded from the root of your working directory; all you need to do is
fill in the necessary parts.

.. note::

    The configuration file is optional, but recommended. If, for any reason, you prefer not to use it, there's always an
    alternative way to configure Pyrogram via Client's parameters. Doing so, you can have full control on how to store
    and load your settings (e.g.: from environment variables).

    Settings specified via Client's parameter have higher priority and will override any setting stored in the
    configuration file.


The config.ini File
-------------------

By default, Pyrogram will look for a file named ``config.ini`` placed at the root of your working directory, that is, in
the same folder of your running script. You can change the name or location of your configuration file by specifying
that in your Client's parameter *config_file*.

-   Replace the default *config.ini* file with *my_configuration.ini*:

    .. code-block:: python

        from pyrogram import Client

        app = Client("my_account", config_file="my_configuration.ini")


Configuration Sections
----------------------

There are all the sections Pyrogram uses in its configuration file:

Pyrogram
^^^^^^^^

The ``pyrogram`` section is used to store Telegram credentials, namely the API Key, which consists of two parts:
*api_id* and *api_hash*.

.. code-block:: ini

    [pyrogram]
    api_id = 12345
    api_hash = 0123456789abcdef0123456789abcdef

`More info <../start/Setup.html#configuration>`_

Proxy
^^^^^

The ``proxy`` section contains settings about your SOCKS5 proxy.

.. code-block:: ini

    [proxy]
    enabled = True
    hostname = 11.22.33.44
    port = 1080
    username = <your_username>
    password = <your_password>


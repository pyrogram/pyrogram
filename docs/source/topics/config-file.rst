Configuration File
==================

As already mentioned in previous pages, Pyrogram can be configured by the use of an INI file.
This page explains how this file is structured, how to use it and why.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Introduction
------------

The idea behind using a configuration file is to help keeping your code free of private settings information such as
the API Key and Proxy, without having you to deal with how to load such settings. The configuration file, usually
referred as ``config.ini`` file, is automatically loaded from the root of your working directory; all you need to do is
fill in the necessary parts.

.. note::

    The configuration file is optional, but recommended. If, for any reason, you prefer not to use it, there's always an
    alternative way to configure Pyrogram via Client's parameters. Doing so, you can have full control on how to store
    and load your settings.

    Settings specified via Client's parameter have higher priority and will override any setting stored in the
    configuration file.


The config.ini File
-------------------

By default, Pyrogram will look for a file named ``config.ini`` placed at the root of your working directory, that is,
the same folder of your running script. You can change the name or location of your configuration file by specifying it
in your Client's parameter *config_file*.

-   Replace the default *config.ini* file with *my_configuration.ini*:

    .. code-block:: python

        from pyrogram import Client

        app = Client("my_account", config_file="my_configuration.ini")


Configuration Sections
----------------------

These are all the sections Pyrogram uses in its configuration file:

Pyrogram
^^^^^^^^

The ``[pyrogram]`` section contains your Telegram API credentials: *api_id* and *api_hash*.

.. code-block:: ini

    [pyrogram]
    api_id = 12345
    api_hash = 0123456789abcdef0123456789abcdef

`More info about API Key. <../intro/setup#api-keys>`_

Proxy
^^^^^

The ``[proxy]`` section contains settings about your SOCKS5 proxy.

.. code-block:: ini

    [proxy]
    enabled = True
    hostname = 11.22.33.44
    port = 1080
    username = <your_username>
    password = <your_password>

`More info about SOCKS5 Proxy. <proxy>`_

Plugins
^^^^^^^

The ``[plugins]`` section contains settings about Smart Plugins.

.. code-block:: ini

    [plugins]
    root = plugins
    include =
        module
        folder.module
    exclude =
        module fn2

`More info about Smart Plugins. <smart-plugins>`_

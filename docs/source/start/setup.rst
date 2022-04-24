Project Setup
=============

We have just :doc:`installed Pyrogram <../intro/install>`. In this page we'll discuss what you need to do in order to set up a
project with the framework.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

API Key
-------

The first step requires you to obtain a valid Telegram API key (api_id and api_hash pair):

#. Visit https://my.telegram.org/apps and log in with your Telegram account.
#. Fill out the form with your details and register a new Telegram application.
#. Done. The API key consists of two parts: **api_id** and **api_hash**. Keep it secret.

.. note::

    The API key defines a token for a Telegram *application* you are going to build.
    This means that you are able to authorize multiple users or bots with a single API key.

Configuration
-------------

Having the API key from the previous step in handy, we can now begin to configure a Pyrogram project: pass your API key to Pyrogram by using the *api_id* and *api_hash* parameters of the Client class:

.. code-block:: python

    from pyrogram import Client

    api_id = 12345
    api_hash = "0123456789abcdef0123456789abcdef"

    app = Client("my_account", api_id=api_id, api_hash=api_hash)
Proxy Settings
==============

Pyrogram supports proxies with and without authentication. This feature allows Pyrogram to exchange data with Telegram
through an intermediate SOCKS 4/5 or HTTP (CONNECT) proxy server.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Usage
-----

To use Pyrogram with a proxy, use the *proxy* parameter in the Client class. If your proxy doesn't require authorization
you can omit ``username`` and ``password``.

.. code-block:: python

    from pyrogram import Client

    proxy = {
        "scheme": "socks5",  # "socks4", "socks5" and "http" are supported
        "hostname": "11.22.33.44",
        "port": 1234,
        "username": "username",
        "password": "password"
    }

   app = Client("my_account", proxy=proxy)

   app.run()

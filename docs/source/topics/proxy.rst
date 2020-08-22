SOCKS5 Proxy
============

Pyrogram supports proxies with and without authentication. This feature allows Pyrogram to exchange data with Telegram
through an intermediate SOCKS5 proxy server.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Usage
-----

-  To use Pyrogram with a proxy, simply append the following to your ``config.ini`` file and replace the values
   with your own settings:

   .. code-block:: ini

       [proxy]
       enabled = True
       hostname = 11.22.33.44
       port = 1080
       username = <your_username>
       password = <your_password>

   To enable or disable the proxy without deleting your settings from the config file,
   change the ``enabled`` value as follows:

      -   ``1``, ``yes``, ``True`` or ``on``: Enables the proxy
      -   ``0``, ``no``, ``False`` or ``off``: Disables the proxy

-  Alternatively, you can setup your proxy without the need of the ``config.ini`` file by using the *proxy* parameter
   in the Client class:

   .. code-block:: python

       from pyrogram import Client

       app = Client(
           session_name="example",
           proxy=dict(
               hostname="11.22.33.44",
               port=1080,
               username="<your_username>",
               password="<your_password>"
           )
       )

       app.start()

       ...

.. note:: If your proxy doesn't require authorization you can omit ``username`` and ``password`` by either leaving the
   values blank/empty or completely delete the lines.
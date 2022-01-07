Pyrogram Client
===============

You have entered the API Reference section where you can find detailed information about Pyrogram's API. The main Client
class, all available methods and types, filters, handlers, decorators and bound-methods detailed descriptions can be
found starting from this page.

This page is about the Client class, which exposes high-level methods for an easy access to the API.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    with app:
        app.send_message("me", "Hi!")

-----

Details
-------

.. autoclass:: pyrogram.Client()

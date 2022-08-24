Speedups
========

Pyrogram's speed can be boosted up by using TgCrypto and uvloop.

-----

TgCrypto
--------

TgCrypto_ is a high-performance, easy-to-install cryptography library specifically written in C for Pyrogram as a Python
extension. It is a replacement for a slower Python-only alternative and implements the cryptographic algorithms Telegram
requires, namely: AES-256-IGE, AES-256-CTR and AES-256-CBC.

Installation
^^^^^^^^^^^^

.. code-block:: bash

    $ pip3 install -U tgcrypto

Usage
^^^^^

Pyrogram will automatically make use of TgCrypto when detected, all you need to do is to install it.

uvloop
------

uvloop_ is a fast, drop-in replacement of the built-in asyncio event loop. uvloop is implemented in Cython and uses
libuv under the hood. It makes asyncio 2-4x faster.

Installation
^^^^^^^^^^^^

.. code-block:: bash

    $ pip3 install -U uvloop

Usage
^^^^^

Call ``uvloop.install()`` before calling ``asyncio.run()`` or ``app.run()``.

.. code-block:: python

    import asyncio
    import uvloop

    from pyrogram import Client


    async def main():
        app = Client("my_account")

        async with app:
            print(await app.get_me())


    uvloop.install()
    asyncio.run(main())

The ``uvloop.install()`` call also needs to be placed before creating a Client instance.

.. code-block:: python

    import uvloop
    from pyrogram import Client

    uvloop.install()

    app = Client("my_account")


    @app.on_message()
    async def hello(client, message):
        print(await client.get_me())


    app.run()

.. _TgCrypto: https://github.com/pyrogram/tgcrypto
.. _uvloop: https://github.com/MagicStack/uvloop

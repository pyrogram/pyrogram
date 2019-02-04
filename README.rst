|header|

Pyrogram
========

.. code-block:: python

    from pyrogram import Client, Filters

    app = Client("my_account")


    @app.on_message(Filters.private)
    def hello(client, message):
        message.reply("Hello {}".format(message.from_user.first_name))


    app.run()

**Pyrogram** is an elegant, easy-to-use Telegram_ client library and framework written from the ground up in Python and C.
It enables you to easily create custom apps using both user and bot identities (bot API alternative) via the `MTProto API`_.

    `A fully-asynchronous variant is also available » <https://github.com/pyrogram/pyrogram/issues/181>`_

Features
--------

-   **Easy**: You can install Pyrogram with pip and start building your applications right away.
-   **Elegant**: Low-level details are abstracted and re-presented in a much nicer and easier way.
-   **Fast**: Crypto parts are boosted up by TgCrypto_, a high-performance library written in pure C.
-   **Documented**: Pyrogram API methods, types and public interfaces are well documented.
-   **Type-hinted**: Exposed Pyrogram types and method parameters are all type-hinted.
-   **Updated**, to the latest Telegram API version, currently Layer 91 on top of `MTProto 2.0`_.
-   **Pluggable**: The Smart Plugin system allows to write components with minimal boilerplate code.
-   **Comprehensive**: Execute any advanced action an official client is able to do, and even more.

Requirements
------------

-   Python 3.4 or higher.
-   A `Telegram API key`_.

Installing
----------

.. code:: shell

    pip3 install pyrogram

Resources
---------

-   The Docs contain lots of resources to help you getting started with Pyrogram: https://docs.pyrogram.ml.
-   Reading `Examples in this repository`_ is also a good way for learning how Pyrogram works.
-   Seeking extra help? Don't be shy, come join and ask our Community_!
-   For other requests you can send an Email_ or a Message_.

Contributing
------------

Pyrogram is brand new, and **you are welcome to try it and help make it even better** by either submitting pull
requests or reporting issues/bugs as well as suggesting best practices, ideas, enhancements on both code
and documentation. Any help is appreciated!

Copyright & License
-------------------

-   Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
-   Licensed under the terms of the `GNU Lesser General Public License v3 or later (LGPLv3+)`_

.. _`Telegram`: https://telegram.org/
.. _`MTProto API`: https://core.telegram.org/api#telegram-api
.. _`Telegram API key`: https://docs.pyrogram.ml/start/ProjectSetup#api-keys
.. _`Community`: https://t.me/PyrogramChat
.. _`Examples in this repository`: https://github.com/pyrogram/pyrogram/tree/master/examples
.. _`GitHub`: https://github.com/pyrogram/pyrogram/issues
.. _`Email`: admin@pyrogram.ml
.. _`Message`: https://t.me/haskell
.. _TgCrypto: https://github.com/pyrogram/tgcrypto
.. _`MTProto 2.0`: https://core.telegram.org/mtproto
.. _`GNU Lesser General Public License v3 or later (LGPLv3+)`: COPYING.lesser

.. |header| raw:: html

    <h1 align="center">
        <a href="https://github.com/pyrogram/pyrogram">
            <div><img src="https://raw.githubusercontent.com/pyrogram/logos/master/logos/pyrogram_logo2.png" alt="Pyrogram Logo"></div>
        </a>
    </h1>

    <p align="center">
        <b>Telegram MTProto API Framework for Python</b>

        <br>
        <a href="https://docs.pyrogram.ml">
            Documentation
        </a>
        •
        <a href="https://github.com/pyrogram/pyrogram/releases">
            Changelog
        </a>
        •
        <a href="https://t.me/PyrogramChat">
            Community
        </a>
        <br>
        <a href="compiler/api/source/main_api.tl">
            <img src="https://img.shields.io/badge/schema-layer%2091-eda738.svg?longCache=true&colorA=262b30"
                alt="Schema Layer">
        </a>
        <a href="https://github.com/pyrogram/tgcrypto">
            <img src="https://img.shields.io/badge/tgcrypto-v1.1.1-eda738.svg?longCache=true&colorA=262b30"
                alt="TgCrypto Version">
        </a>
    </p>

.. |logo| image:: https://raw.githubusercontent.com/pyrogram/logos/master/logos/pyrogram_logo2.png
    :target: https://pyrogram.ml
    :alt: Pyrogram

.. |description| replace:: **Telegram MTProto API Framework for Python**

.. |schema| image:: https://img.shields.io/badge/schema-layer%2091-eda738.svg?longCache=true&colorA=262b30
    :target: compiler/api/source/main_api.tl
    :alt: Schema Layer

.. |tgcrypto| image:: https://img.shields.io/badge/tgcrypto-v1.1.1-eda738.svg?longCache=true&colorA=262b30
    :target: https://github.com/pyrogram/tgcrypto
    :alt: TgCrypto Version

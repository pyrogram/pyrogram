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

**Pyrogram** is a brand new Telegram_ Client Library written from the ground up in Python and C. It can be used for
building custom Telegram applications that interact with the MTProto API as both User and Bot.

Features
--------

-   **Easy to use**: You can easily install Pyrogram using pip and start building your app right away.
-   **High-level**: The low-level details of MTProto are abstracted and automatically handled.
-   **Fast**: Crypto parts are boosted up by TgCrypto_, a high-performance library written in pure C.
-   **Updated** to the latest Telegram API version, currently Layer 91 on top of MTProto 2.0.
-   **Documented**: The Pyrogram API is well documented and resembles the Telegram Bot API.
-   **Full API**, allowing to execute any advanced action an official client is able to do, and more.

Requirements
------------

-   Python 3.4 or higher.
-   A `Telegram API key`_.

Installing
----------

.. code:: shell

    pip3 install pyrogram

Getting Started
---------------

-   The Docs contain lots of resources to help you getting started with Pyrogram: https://docs.pyrogram.ml.
-   Reading Examples_ in this repository is also a good way for learning how things work.
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
.. _`Telegram API key`: https://docs.pyrogram.ml/start/ProjectSetup#api-keys
.. _`Community`: https://t.me/PyrogramChat
.. _`Examples`: https://github.com/pyrogram/pyrogram/tree/master/examples
.. _`GitHub`: https://github.com/pyrogram/pyrogram/issues
.. _`Email`: admin@pyrogram.ml
.. _`Message`: https://t.me/haskell
.. _TgCrypto: https://github.com/pyrogram/tgcrypto
.. _`GNU Lesser General Public License v3 or later (LGPLv3+)`: COPYING.lesser

.. |header| raw:: html

    <h1 align="center">
        <a href="https://github.com/pyrogram/pyrogram">
            <div><img src="https://raw.githubusercontent.com/pyrogram/logos/master/logos/pyrogram_logo2.png" alt="Pyrogram Logo"></div>
        </a>
    </h1>

    <p align="center">
        <b>Telegram MTProto API Client Library for Python</b>

        <br>
        <a href="https://github.com/pyrogram/pyrogram/releases/latest">
            Download
        </a>
        •
        <a href="https://docs.pyrogram.ml">
            Documentation
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
                alt="TgCrypto">
        </a>
    </p>

.. |logo| image:: https://raw.githubusercontent.com/pyrogram/logos/master/logos/pyrogram_logo2.png
    :target: https://pyrogram.ml
    :alt: Pyrogram

.. |description| replace:: **Telegram MTProto API Client Library for Python**

.. |scheme| image:: "https://img.shields.io/badge/schema-layer%2091-eda738.svg?longCache=true&colorA=262b30"
    :target: compiler/api/source/main_api.tl
    :alt: Scheme Layer

.. |tgcrypto| image:: "https://img.shields.io/badge/tgcrypto-v1.1.1-eda738.svg?longCache=true&colorA=262b30"
    :target: https://github.com/pyrogram/tgcrypto
    :alt: TgCrypto

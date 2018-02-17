|header|

Table of Contents
=================

-   `About`_

    -   `Features`_

    -   `Requirements`_

-   `Getting Started`_
    
    -   `Installation`_
    
    -   `Configuration`_
    
    -   `Usage`_

-   `Documentation`_

-   `Contribution`_

-   `Feedback`_

-   `License`_


About
=====

**Pyrogram** is a fully functional Telegram Client Library written from the ground up in Python.
It offers simple and complete access to the `Telegram Messenger API`_ and is designed for Python
developers keen on building custom Telegram applications.


Features
--------

-   **Easy to setup**: Pyrogram can be easily installed and upgraded using **pip**, requires
    a minimal set of dependencies (which are also automatically managed) and very few lines
    of code to get started with.

-   **Easy to use**: Pyrogram provides idiomatic, developer-friendly, clean and readable
    Python code (either generated or hand-written) making the Telegram API simple to use.

-   **High level**: Pyrogram automatically handles all the low-level details of
    communication with the Telegram servers by implementing the
    `MTProto Mobile Protocol v2.0`_ and the mechanisms needed for establishing
    a reliable connection.

-   **Fast**: Pyrogram's speed is boosted up by `TgCrypto`_, a high-performance, easy-to-install
    Telegram Crypto Library written in C as a Python extension.

-   **Updated**: Pyrogram makes use of the latest Telegram API version, currently `Layer 75`_.

-   **Documented**: Pyrogram API public methods are documented and resemble the well
    established Telegram Bot API, thus offering a familiar look to Bot developers.

-   **Full API support**: Beside the simple, bot-like methods offered by the Pyrogram API,
    the library also provides a complete, low-level access to every single Telegram API method.


Requirements
------------

-   Python 3.3 or higher.

-   A Telegram API key.
    

Getting Started
===============

Installation
------------

-   You can easily install and upgrade the library using standard Python tools:

    .. code:: shell

        $ pip install --upgrade pyrogram
        
-   Or, with TgCrypto_:

    .. code:: shell

        $ pip install --upgrade pyrogram[tgcrypto]

Configuration
-------------

-   Create a new ``config.ini`` file at the root of your working directory, copy-paste
    the following and replace the **api_id** and **api_hash** values with `your own`_:

    .. code:: ini

        [pyrogram]
        api_id = 12345
        api_hash = 0123456789abcdef0123456789abcdef

Usage
-----

-   And here's how Pyrogram looks like:

    .. code:: python

        from pyrogram import Client

        client = Client("example")
        client.start()

        client.send_message("me", "Hi there! I'm using Pyrogram")
        client.send_photo("me", "/home/dan/pic.jpg", "Nice photo!")

        client.stop()
    
That's all you need for getting started with Pyrogram. For more detailed information,
please refer to the Documentation_.


Documentation
=============

- The entire Pyrogram's documentation resides at https://docs.pyrogram.ml.


Contribution
============

**You are very welcome to contribute** by either submitting pull requests or
reporting issues/bugs as well as suggesting best practices, ideas, enhancements
on both code and documentation. Any help is appreciated!


Feedback
========

Means for getting in touch:

-   `Community`_
-   `Telegram`_
-   `GitHub`_
-   `Email`_


License
=======

-   Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>

-   Licensed under the terms of the
    `GNU Lesser General Public License v3 or later (LGPLv3+)`_
    

.. _`Telegram Messenger API`: https://core.telegram.org/api#telegram-api

.. _`MTProto Mobile Protocol v2.0`: https://core.telegram.org/mtproto

.. _`Layer 75`: compiler/api/source/main_api.tl

.. _`your own`: https://github.com/pyrogram/pyrogram/wiki/Getting-Started#api-keys

.. _`Introduction`: https://github.com/pyrogram/pyrogram/wiki/Getting-Started

.. _`Telegram`: https://t.me/haskell

.. _`Community`: https://t.me/PyrogramChat

.. _`bot-like`: https://core.telegram.org/bots/api#available-methods

.. _`GitHub`: https://github.com/pyrogram/pyrogram/issues

.. _`Email`: admin@pyrogram.ml

.. _TgCrypto: https://docs.pyrogram.ml/resources/TgCrypto

.. _`GNU Lesser General Public License v3 or later (LGPLv3+)`: COPYING.lesser

.. |header| raw:: html

    <h1 align="center">
        <a href="https://pyrogram.ml">
            <div><img src="https://pyrogram.ml/images/icon.png" alt="Pyrogram Icon"></div>
            <div><img src="https://pyrogram.ml/images/label.png" alt="Pyrogram Label"></div>
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
        </a
        <br><br><br>
        <a href="compiler/api/source/main_api.tl">
            <img src="https://www.pyrogram.ml/images/scheme.svg"
                alt="Scheme Layer 75">
        </a>
        <a href="https://github.com/pyrogram/tgcrypto">
            <img src="https://www.pyrogram.ml/images/tgcrypto.svg"
                alt="TgCrypto">
        </a>
    </p>

.. |logo| image:: https://pyrogram.ml/images/logo.png
    :target: https://pyrogram.ml
    :alt: Pyrogram

.. |description| replace:: **Telegram MTProto API Client Library for Python**

.. |scheme| image:: https://www.pyrogram.ml/images/scheme.svg
    :target: compiler/api/source/main_api.tl
    :alt: Scheme Layer 75

.. |tgcrypto| image:: https://www.pyrogram.ml/images/tgcrypto.svg
    :target: https://github.com/pyrogram/tgcrypto
    :alt: TgCrypto

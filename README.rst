|header|

Table of Contents
=================

-   `Overview`_

-   `Requirements`_

-   `Installation`_

-   `Getting Started`_

-   `Development`_

-   `Documentation`_

-   `Contribution`_

-   `Feedback`_

-   `License`_


Overview
========

**Pyrogram** is a Client Library written from the ground up in Python, designed
for Python application developers. It offers simple and complete access to the
`Telegram Messenger API`_. Pyrogram:

-   Provides idiomatic, developer-friendly Python code (either generated or
    hand-written) making the Telegram API simple to use.

-   Handles all the low-level details of communication with the Telegram servers
    by implementing the `MTProto Mobile Protocol v2.0`_.

-   Makes use of the latest Telegram API version (`Layer 73`_).

-   Can be easily installed and upgraded using ``pip``.

-   Requires a minimal set of dependencies.


Requirements
============

-   Operating systems:

    -   Linux

    -   macOS

    -   Windows

-   Python 3.3 or higher.

-   A Telegram API key.


Installation
============

You can install and upgrade the library using standard Python tools:

.. code:: shell

    $ pip install --upgrade pyrogram


Getting Started
===============

The `Wiki`_ contains all the information needed to get you started with Pyrogram:

-   `Getting Started`_


Development
===========

The library is still in its early stages, thus lots of functionalities aiming to
make working with Telegram's API easy are yet to be added and documented.

However, being the core functionalities already implemented, every Telegram API
method listed in the API scheme can be used right away; the goal is therefore to
build a powerful, simple to use, `bot-like`_ interface on top of those low-level
functions.


Documentation
=============

Soon. For now, have a look at the ``pyrogram.Client`` code to get some insights.

Currently you are able to easily:

-   ``send_message``

-   ``forward_messages``

-   ``edit_message_text``

-   ``delete_messages``

-   ``send_chat_action``

-   Some more...

as well as listening for updates and catching API errors.


Contribution
============

**You are very welcome to contribute** by either submitting pull requests or
reporting issues/bugs as well as suggesting best practices, ideas, enhancements
on both code and documentation. Any help is appreciated!


Feedback
========

Means for getting in touch:

-   `Telegram`_
-   `GitHub`_
-   `Email`_


License
=======

-   Copyright (C) 2017 Dan Tès <https://github.com/delivrance>

-   Licensed under the terms of the
    `GNU Lesser General Public License v3 or later (LGPLv3+)`_
    

.. _`Telegram Messenger API`: https://core.telegram.org/api#telegram-api

.. _`MTProto Mobile Protocol v2.0`: https://core.telegram.org/mtproto

.. _`Layer 73`: compiler/api/source/main_api.tl

.. _`Wiki`: https://github.com/pyrogram/pyrogram/wiki

.. _`Getting Started`: https://github.com/pyrogram/pyrogram/wiki/Getting-Started

.. _`Telegram`: https://t.me/joinchat/AWDQ8lK2HgBN7ka4OyWVTw

.. _`bot-like`: https://core.telegram.org/bots/api#available-methods

.. _`GitHub`: https://github.com/pyrogram/pyrogram/issues

.. _`Email`: admin@pyrogram.ml

.. _`GNU Lesser General Public License v3 or later (LGPLv3+)`: COPYING.lesser

.. |header| raw:: html

    <h1 align="center">
        <a href="https://pyrogram.ml">
            <img src="https://pyrogram.ml/images/logo.png" alt="Pyrogram">
        </a>
    </h1>

    <p align="center">
        <b>Telegram MTProto API Client Library for Python</b>
        <br>
        <a href="https://github.com/pyrogram/pyrogram/wiki">
            Wiki
        </a>
        •
        <a href="https://t.me/joinchat/AWDQ8lK2HgBN7ka4OyWVTw">
            Telegram Group
        </a
        <br><br><br>
        <a href="compiler/api/source/main_api.tl">
            <img src="https://img.shields.io/badge/scheme-layer%2073-eda738.svg?style=for-the-badge&colorA=262b30"
                alt="Scheme Layer 73">
        </a>
        <a href="https://core.telegram.org/mtproto">
            <img src="https://img.shields.io/badge/mtproto-v2.0-eda738.svg?style=for-the-badge&colorA=262b30"
                alt="MTProto v2.0">
        </a>
    </p>

.. |logo| image:: https://pyrogram.ml/images/logo.png
    :target: https://pyrogram.ml
    :alt: Pyrogram

.. |description| replace:: **Telegram MTProto API Client Library for Python**

.. |scheme| image:: https://img.shields.io/badge/scheme-layer%2073-eda738.svg?style=for-the-badge&colorA=262b30
    :target: compiler/api/source/main_api.tl
    :alt: Scheme Layer 73

.. |mtproto| image:: https://img.shields.io/badge/mtproto-v2.0-eda738.svg?style=for-the-badge&colorA=262b30
    :target: https://core.telegram.org/mtproto
    :alt: MTProto v2.0

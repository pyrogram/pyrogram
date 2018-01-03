|header|

Table of Contents
=================

-   `Overview`_

    -   `Features`_

    -   `Requirements`_

-   `Getting Started`_
    
    -   `Installation`_
    
    -   `Setup`_
    
    -   `Usage`_

-   `Development`_

-   `Documentation`_

-   `Contribution`_

-   `Feedback`_

-   `License`_


Overview
========

**Pyrogram** is a fully functional Telegram Client Library written from the ground up in Python.
It offers simple and complete access to the `Telegram Messenger API`_ and is designed for Python
developers keen on building custom Telegram applications.


Features
--------

-   **Easy to setup**: Pyrogram can be easily installed and upgraded using ``pip``, requires
    a minimal set of dependencies (which are also automatically managed) and very few lines
    of code to get started with.

-   **Easy to use**: Pyrogram provides idiomatic, developer-friendly, clean and readable
    Python code (either generated or hand-written) making the Telegram API simple to use.
    
-   **High level**: Pyrogram automatically handles all the low-level details of
    communication with the Telegram servers by implementing the
    `MTProto Mobile Protocol v2.0`_ and the mechanisms needed for establishing
    a reliable connection.
    
-   **Updated**: Pyrogram makes use of the latest Telegram API version, currently `Layer 74`_.
    
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

Setup
-----

-   Create a new ``config.ini`` file at the root of your working directory, copy-paste
    the following and replace the **api_id** and **api_hash** values with `your own`_:

    .. code:: ini

        [pyrogram]
        api_id = 12345
        api_hash = 0123456789abcdef0123456789abcdef

Usage
-----

-   You can now start by running the code below from a new Python file.

    .. code:: python

        from pyrogram import Client
        
        # Create and start a new Client
        client = Client(session_name="example")
        client.start()

        # Send a text message to yourself (Saved Messages)
        client.send_message(
            chat_id="me",
            text="Hi there! I'm using Pyrogram"
        )
        
        # When done, stop the Client
        client.stop()
    
That's all you need for getting started with Pyrogram. For more detailed information,
please refer to the documentation:

-   Wiki: `Introduction`_.
-   Docs: https://docs.pyrogram.ml.

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

- Pyrogram's API documentation at https://docs.pyrogram.ml.
- Guides and examples can be found on the `Wiki`_.


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

-   Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>

-   Licensed under the terms of the
    `GNU Lesser General Public License v3 or later (LGPLv3+)`_
    

.. _`Telegram Messenger API`: https://core.telegram.org/api#telegram-api

.. _`MTProto Mobile Protocol v2.0`: https://core.telegram.org/mtproto

.. _`Layer 74`: compiler/api/source/main_api.tl

.. _`Wiki`: https://github.com/pyrogram/pyrogram/wiki

.. _`your own`: https://github.com/pyrogram/pyrogram/wiki/Getting-Started#api-keys

.. _`Introduction`: https://github.com/pyrogram/pyrogram/wiki/Getting-Started

.. _`Telegram`: https://t.me/haskell

.. _`bot-like`: https://core.telegram.org/bots/api#available-methods

.. _`GitHub`: https://github.com/pyrogram/pyrogram/issues

.. _`Email`: admin@pyrogram.ml

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
        <a href="https://pypi.python.org/pypi/Pyrogram">
            Download
        </a>
        •
        <a href="https://github.com/pyrogram/pyrogram/wiki">
            Wiki
        </a>
        •
        <a href="https://docs.pyrogram.ml">
            Documentation
        </a>
        •
        <a href="https://t.me/joinchat/AWDQ8lK2HgBN7ka4OyWVTw">
            Community
        </a
        <br><br><br>
        <a href="compiler/api/source/main_api.tl">
            <img src="https://www.pyrogram.ml/images/scheme.svg"
                alt="Scheme Layer 74">
        </a>
        <a href="https://core.telegram.org/mtproto">
            <img src="https://www.pyrogram.ml/images/mtproto.svg"
                alt="MTProto v2.0">
        </a>
    </p>

.. |logo| image:: https://pyrogram.ml/images/logo.png
    :target: https://pyrogram.ml
    :alt: Pyrogram

.. |description| replace:: **Telegram MTProto API Client Library for Python**

.. |scheme| image:: https://www.pyrogram.ml/images/scheme.svg
    :target: compiler/api/source/main_api.tl
    :alt: Scheme Layer 74

.. |mtproto| image:: https://www.pyrogram.ml/images/mtproto.svg
    :target: https://core.telegram.org/mtproto
    :alt: MTProto v2.0

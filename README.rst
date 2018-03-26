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

**Pyrogram** is a brand new Telegram_ Client Library written from the ground up in Python and C. It can be used for building
custom Telegram applications in Python that interact with the MTProto API as both User and Bot.

Features
--------

-   **Easy to setup**: Pyrogram can be easily installed using pip and requires very few lines of code to get started with.
    
-   **Easy to use**: Pyrogram provides idiomatic, clean and readable Python code making the Telegram API simple to use.

-   **High-level**: Pyrogram automatically handles all the low-level details of communication with Telegram servers.

-   **Updated**: Pyrogram makes use of the latest Telegram MTProto API version, currently Layer 76.

-   **Fast**: Pyrogram critical parts are boosted up by `TgCrypto`_, a high-performance Crypto Library written in pure C.
    
-   **Documented**: Pyrogram API methods are documented and resemble the well established Telegram Bot API,
    thus offering a familiar look to Bot developers.

-   **Full API support**: Beside the simple Bot API-like methods, Pyrogram also provides an easy access to every single
    Telegram MTProto API method allowing you to programmatically execute any action an official client is able to do, and more.


Requirements
------------

-   Python 3.4 or higher.

-   A Telegram API key.
    

Getting Started
===============

Installation
------------

-   You can install and upgrade Pyrogram using pip:

    .. code:: shell

        $ pip3 install --upgrade pyrogram

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

-   And here is how Pyrogram looks like:

    .. code:: python

        from pyrogram import Client

        client = Client("example")
        client.start()

        client.send_message("me", "Hi there! I'm using Pyrogram")

        client.stop()
    
That's all you need for getting started with Pyrogram. For more detailed information,
please refer to the Documentation_ and the Examples_ folder.


Documentation
=============

- The entire Pyrogram documentation resides at https://docs.pyrogram.ml.


Contribution
============

Pyrogram is brand new! **You are welcome to try it and help make it better** by either submitting pull
requests or reporting issues/bugs as well as suggesting best practices, ideas, enhancements on both code
and documentation. Any help is appreciated!


Feedback
========

Means for getting in touch:

-   `Community`_
-   `GitHub`_
-   `Email`_


License
=======

-   Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>

-   Licensed under the terms of the
    `GNU Lesser General Public License v3 or later (LGPLv3+)`_
    

.. _`Telegram`: https://telegram.org/

.. _`your own`: https://docs.pyrogram.ml/start/ProjectSetup#api-keys

.. _`Examples`: https://github.com/pyrogram/pyrogram/blob/master/examples/README.md

.. _`Community`: https://t.me/PyrogramChat

.. _`bot-like`: https://core.telegram.org/bots/api#available-methods

.. _`GitHub`: https://github.com/pyrogram/pyrogram/issues

.. _`Email`: admin@pyrogram.ml

.. _TgCrypto: https://github.com/pyrogram/tgcrypto

.. _`GNU Lesser General Public License v3 or later (LGPLv3+)`: COPYING.lesser

.. |header| raw:: html

    <h1 align="center">
        <a href="https://github.com/pyrogram/pyrogram">
            <div><img src="https://media.pyrogram.ml/images/icon.png" alt="Pyrogram Icon"></div>
            <div><img src="https://media.pyrogram.ml/images/label.png" alt="Pyrogram Label"></div>
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
        <br><br>
        <a href="compiler/api/source/main_api.tl">
            <img src="https://media.pyrogram.ml/images/scheme.svg"
                alt="Scheme Layer 76">
        </a>
        <a href="https://github.com/pyrogram/tgcrypto">
            <img src="https://media.pyrogram.ml/images/tgcrypto.svg"
                alt="TgCrypto">
        </a>
    </p>

.. |logo| image:: https://pyrogram.ml/images/logo.png
    :target: https://pyrogram.ml
    :alt: Pyrogram

.. |description| replace:: **Telegram MTProto API Client Library for Python**

.. |scheme| image:: https://www.pyrogram.ml/images/scheme.svg
    :target: compiler/api/source/main_api.tl
    :alt: Scheme Layer 76

.. |tgcrypto| image:: https://www.pyrogram.ml/images/tgcrypto.svg
    :target: https://github.com/pyrogram/tgcrypto
    :alt: TgCrypto

Welcome to Pyrogram
===================

.. raw:: html

    <p align="right">
        <a class="github-button" href="https://github.com/pyrogram/pyrogram/subscription" data-icon="octicon-eye" data-size="large" data-show-count="true" aria-label="Watch pyrogram/pyrogram on GitHub">Watch</a>
        <a class="github-button" href="https://github.com/pyrogram/pyrogram" data-icon="octicon-star" data-size="large" data-show-count="true" aria-label="Star pyrogram/pyrogram on GitHub">Star</a>
        <a class="github-button" href="https://github.com/pyrogram/pyrogram/fork" data-icon="octicon-repo-forked" data-size="large" data-show-count="true" aria-label="Fork pyrogram/pyrogram on GitHub">Fork</a>
    </p>

    <div align="center">
        <a href="https://pyrogram.ml">
            <div><img src="https://pyrogram.ml/images/icon.png" alt="Pyrogram Icon"></div>
            <div><img src="https://pyrogram.ml/images/label.png" alt="Pyrogram Label"></div>
        </a>
    </div>

    <p align="center">
        <b>Telegram MTProto API Client Library for Python</b>
        <br>
        <a href="https://github.com/pyrogram/pyrogram/releases/latest">
            Download
        </a>
        •
        <a href="https://github.com/pyrogram/pyrogram">
            Source code
        </a>
        •
        <a href="https://t.me/PyrogramChat">
            Community
        </a>
        <br><br>
        <a href="https://github.com/pyrogram/pyrogram/blob/master/compiler/api/source/main_api.tl">
            <img src="https://www.pyrogram.ml/images/scheme.svg"
                alt="Scheme Layer 75">
        </a>
        <a href="https://github.com/pyrogram/tgcrypto">
            <img src="https://www.pyrogram.ml/images/tgcrypto.svg"
                alt="TgCrypto">
        </a>
    </p>

About
-----

Pyrogram is a fully functional Telegram Client Library written from the ground up in Python.
It offers **simple** and **complete** access to the Telegram Messenger API and is designed for Python developers
keen on building custom Telegram applications.

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

Preview
-------

.. code-block:: python

    from pyrogram import Client

    client = Client("example")
    client.start()

    client.send_message("me", "Hi there! I'm using Pyrogram")
    client.send_photo("me", "/home/dan/pic.jpg", "Nice photo!")

    client.stop()

To get started, press Next.

.. toctree::
    :hidden:
    :caption: Getting Started

    start/QuickInstallation
    start/ProjectSetup
    start/BasicUsage

.. toctree::
    :hidden:
    :caption: Resources

    resources/TextFormatting
    resources/UpdateHandling
    resources/ErrorHandling
    resources/SOCKS5Proxy
    resources/AutoAuthorization
    resources/TgCrypto

.. toctree::
    :hidden:
    :caption: Main Package

    pyrogram/index

.. toctree::
    :hidden:
    :caption: Telegram API

    functions/index
    types/index

.. _`MTProto Mobile Protocol v2.0`: https://core.telegram.org/mtproto

.. _TgCrypto: https://docs.pyrogram.ml/resources/FastCrypto/

.. _`Layer 75`: https://github.com/pyrogram/pyrogram/blob/master/compiler/api/source/main_api.tl
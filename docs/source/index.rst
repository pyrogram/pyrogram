Welcome to Pyrogram
===================

.. raw:: html

    <div align="center">
        <a href="https://docs.pyrogram.ml">
            <div><img src="_static/logo.png" alt="Pyrogram Logo"></div>
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
        <br>
        <a href="https://github.com/pyrogram/pyrogram/blob/master/compiler/api/source/main_api.tl">
            <img src="https://img.shields.io/badge/schema-layer%2091-eda738.svg?longCache=true&colorA=262b30"
                alt="Scheme Layer">
        </a>
        <a href="https://github.com/pyrogram/tgcrypto">
            <img src="https://img.shields.io/badge/tgcrypto-v1.1.1-eda738.svg?longCache=true&colorA=262b30"
                alt="TgCrypto">
        </a>
    </p>

.. code-block:: python

    from pyrogram import Client, Filters

    app = Client("my_account")


    @app.on_message(Filters.private)
    def hello(client, message):
        message.reply("Hello {}".format(message.from_user.first_name))


    app.run()

Welcome to Pyrogram's Documentation! Here you can find resources for learning how to use the library.
Contents are organized into self-contained topics and can be accessed from the sidebar, or by following them in order
using the Next button at the end of each page. But first, here's a brief overview of what is this all about.

About
-----

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

To get started, press the Next button.

.. toctree::
    :hidden:
    :caption: Quick Start

    start/Installation
    start/Setup
    start/Usage

.. toctree::
    :hidden:
    :caption: Resources

    resources/UpdateHandling
    resources/UsingFilters
    resources/SmartPlugins
    resources/AutoAuthorization
    resources/CustomizeSessions
    resources/TgCrypto
    resources/TextFormatting
    resources/SOCKS5Proxy
    resources/BotsInteraction
    resources/ErrorHandling
    resources/TestServers
    resources/Changelog

.. toctree::
    :hidden:
    :caption: Main Package

    pyrogram/index

.. toctree::
    :hidden:
    :caption: Telegram API

    functions/index
    types/index

.. _`Telegram`: https://telegram.org/
.. _TgCrypto: https://docs.pyrogram.ml/resources/TgCrypto/
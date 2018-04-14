Welcome to Pyrogram
===================

.. raw:: html

    <div align="center">
        <a href="https://docs.pyrogram.ml">
            <div><img src="https://media.pyrogram.ml/images/icon.png" alt="Pyrogram Icon"></div>
            <div><img src="https://media.pyrogram.ml/images/label.png" alt="Pyrogram Label"></div>
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
            <img src="https://media.pyrogram.ml/images/scheme.svg"
                alt="Scheme Layer 75">
        </a>
        <a href="https://github.com/pyrogram/tgcrypto">
            <img src="https://media.pyrogram.ml/images/tgcrypto.svg"
                alt="TgCrypto">
        </a>
    </p>

.. code-block:: python

    from pyrogram import Client, Filters

    app = Client("my_account")


    @app.on_message(Filters.private)
    def hello(client, message):
        client.send_message(
            message.chat.id, "Hello {}".format(message.from_user.first_name))


    app.start()
    app.idle()

Welcome to Pyrogram's Documentation! Here you can find resources for learning how to use the library.
Contents are organized by topic and can be accessed from the sidebar, or by following them one by one using the Next
button at the end of each page. But first, here's a brief overview of what is this all about:

**Pyrogram** is a brand new Telegram_ Client Library written from the ground up in Python and C. It can be used for building
custom Telegram applications that interact with the MTProto API as both User and Bot.

Awesomeness
-----------

-   📦 **Easy to use**: You can easily install Pyrogram using pip and start building your app right away.
-   🚀 **High-level**: All the low-level details of communication with Telegram servers are automatically handled.
-   ⚡️ **Fast**: Critical parts are boosted up by TgCrypto_, a high-performance Crypto Library written in pure C.
-   🔄 **Updated** to the latest Telegram MTProto API version, currently Layer 76.
-   📖 **Documented**: Pyrogram public API methods are documented and resemble the Telegram Bot API.
-   🔋 **Full API**, allows to execute any advanced action an official client is able to do, and more.

To get started, press the Next button.

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
    resources/BotsInteraction

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

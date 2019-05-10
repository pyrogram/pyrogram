Welcome to Pyrogram
===================

.. raw:: html

    <div align="center">
        <a href="https://docs.pyrogram.ml">
            <div><img src="_static/logo.png" alt="Pyrogram Logo"></div>
        </a>
    </div>

    <p align="center">
        <b>Telegram MTProto API Framework for Python</b>

        <br>
        <a href="https://github.com/pyrogram/pyrogram">
            GitHub
        </a>
        •
        <a href="https://t.me/PyrogramChat">
            Community
        </a>

        •
        <a href="https://github.com/pyrogram/pyrogram/releases">
            Changelog
        </a>
        •
        <a href="https://pypi.org/project/Pyrogram">
            PyPI
        </a>
        <br>
        <a href="compiler/api/source/main_api.tl">
            <img src="https://img.shields.io/badge/schema-layer%2097-eda738.svg?longCache=true&colorA=262b30"
                alt="Schema Layer">
        </a>
        <a href="https://github.com/pyrogram/tgcrypto">
            <img src="https://img.shields.io/badge/tgcrypto-v1.1.1-eda738.svg?longCache=true&colorA=262b30"
                alt="TgCrypto Version">
        </a>
    </p>

.. code-block:: python

    from pyrogram import Client, Filters

    app = Client("my_account")


    @app.on_message(Filters.private)
    def hello(client, message):
        message.reply("Hello {}".format(message.from_user.first_name))


    app.run()

**Pyrogram** is an elegant, easy-to-use Telegram_ client library and framework written from the ground up in Python and C.
It enables you to easily create custom apps using both user and bot identities (bot API alternative) via the `MTProto API`_.

How the documentation is organized
----------------------------------

Contents are organized into self-contained topics and can be accessed from the sidebar, or by following them in order
using the Next button at the end of each page.

Relevant Pages
^^^^^^^^^^^^^^

- `Quick Start`_ - Concise steps to get you started as fast as possible.
- `API Usage`_ - Guide on how to use Pyrogram's API.
- `Update Handling`_ - Guide on how to handle Telegram updates.
- Client_ - Reference details about the Client class.
- Types_ - All the available Pyrogram types.
- Methods_ - All the available Pyrogram methods.

**To get started, press the Next button**

.. toctree::
    :hidden:
    :caption: Introduction

    intro/start
    intro/install
    intro/setup
    intro/auth

.. toctree::
    :hidden:
    :caption: Topic Guides

    topics/usage
    topics/update-handling
    topics/using-filters
    topics/more-on-updates
    topics/configuration-file
    topics/smart-plugins
    topics/auto-authorization
    topics/customize-sessions
    topics/tgcrypto
    topics/text-formatting
    topics/socks5-proxy
    topics/bots-interaction
    topics/error-handling
    topics/test-servers
    topics/advanced-usage
    topics/voice-calls
    topics/changelog

.. toctree::
    :hidden:
    :caption: API Reference

    core/client
    core/types
    core/methods
    core/handlers
    core/decorators
    core/filters
    core/errors

.. toctree::
    :hidden:
    :caption: Telegram API

    functions/index
    types/index

.. _Telegram: https://telegram.org
.. _TgCrypto: https://docs.pyrogram.ml/resources/TgCrypto
.. _MTProto API: https://core.telegram.org/api#telegram-api
.. _Quick Start: intro/start.html
.. _API Usage: topics/usage.html
.. _Update Handling: topics/update-handling.html
.. _Client: core/client.html
.. _Types: core/types.html
.. _Methods: core/methods

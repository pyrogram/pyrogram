Welcome to Pyrogram
===================

.. raw:: html

    <div align="center">
        <a href="https://docs.pyrogram.org">
            <div><img src="_static/logo.png" alt="Pyrogram Logo"></div>
        </a>
    </div>

    <p align="center">
        <b>Telegram MTProto API Framework for Python</b>

        <br>
        <a href="https://github.com/pyrogram/pyrogram">
            Source Code
        </a>
        •
        <a href="https://github.com/pyrogram/pyrogram/releases">
            Releases
        </a>
        •
        <a href="https://t.me/Pyrogram">
            Community
        </a>
    </p>

.. code-block:: python

    from pyrogram import Client, Filters

    app = Client("my_account")


    @app.on_message(Filters.private)
    def hello(client, message):
        message.reply("Hello {}".format(message.from_user.first_name))


    app.run()

**Pyrogram** is an elegant, easy-to-use Telegram_ client library and framework written from the ground up in Python and
C. It enables you to easily create custom apps for both user and bot identities (bot API alternative) via the
`MTProto API`_.

.. _Telegram: https://telegram.org
.. _MTProto API: topics/mtproto-vs-botapi#what-is-the-mtproto-api

How the Documentation is Organized
----------------------------------

Contents are organized into self-contained topics and can be all accessed from the sidebar, or by following them in
order using the Next button at the end of each page. Here below you can, instead, find a list of the most relevant
pages for a quick access.

First Steps
^^^^^^^^^^^

- `Quick Start`_ - Overview to get you started quickly.
- `Calling Methods`_ - How to call Pyrogram's methods.
- `Handling Updates`_ - How to handle Telegram updates.
- `Error Handling`_ - How to handle API errors correctly.

.. _Quick Start: intro/quickstart
.. _Calling Methods: start/invoking
.. _Handling Updates: start/updates
.. _Error Handling: start/errors

API Reference
^^^^^^^^^^^^^

- `Client Class`_ - Reference details about the Client class.
- `Available Methods`_ - A list of available high-level methods.
- `Available Types`_ - A list of available high-level types.
- `Bound Methods`_ - A list of convenient bound methods.

.. _Client Class: api/client
.. _Available Methods: api/methods
.. _Available Types: api/types
.. _Bound Methods: api/bound-methods

Meta
^^^^

- `Pyrogram FAQ`_ - Answers to common Pyrogram questions.
- `Pyrogram Glossary`_ - A list of words with brief explanations.
- `Release Notes`_ - Release notes for Pyrogram releases.
- `Powered by Pyrogram`_ - A collection of Pyrogram Projects.
- `Support Pyrogram Development`_ - Ways to show your appreciation.

.. _Pyrogram FAQ: meta/faq
.. _Pyrogram Glossary: meta/glossary
.. _Release Notes: meta/releases
.. _Powered by Pyrogram: meta/powered-by
.. _Support Pyrogram Development: meta/support-pyrogram

.. toctree::
    :hidden:
    :caption: Introduction

    intro/quickstart
    intro/install
    intro/setup

.. toctree::
    :hidden:
    :caption: Getting Started

    start/auth
    start/invoking
    start/updates
    start/errors

.. toctree::
    :hidden:
    :caption: API Reference

    api/client
    api/methods
    api/types
    api/bound-methods
    api/handlers
    api/decorators
    api/filters
    api/errors

.. toctree::
    :hidden:
    :caption: Topic Guides

    topics/filters
    topics/more-on-updates
    topics/config-file
    topics/smart-plugins
    topics/auto-auth
    topics/session-settings
    topics/tgcrypto
    topics/text-formatting
    topics/proxy
    topics/bots-interaction
    topics/mtproto-vs-botapi
    topics/test-servers
    topics/advanced-usage
    topics/voice-calls

.. toctree::
    :hidden:
    :caption: Meta

    meta/faq
    meta/glossary
    meta/releases
    meta/powered-by
    meta/support-pyrogram

.. toctree::
    :hidden:
    :caption: Telegram API

    telegram/functions/index
    telegram/types/index
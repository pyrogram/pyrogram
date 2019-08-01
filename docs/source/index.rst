Welcome to Pyrogram
===================

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
    api/methods/index
    api/types/index
    api/bound-methods/index
    api/handlers
    api/decorators
    api/errors
    api/filters

.. toctree::
    :hidden:
    :caption: Topic Guides

    topics/use-filters
    topics/create-filters
    topics/more-on-updates
    topics/config-file
    topics/smart-plugins
    topics/auto-auth
    topics/session-settings
    topics/tgcrypto
    topics/storage-engines
    topics/text-formatting
    topics/serializing
    topics/proxy
    topics/scheduling
    topics/bots-interaction
    topics/mtproto-vs-botapi
    topics/debugging
    topics/test-servers
    topics/advanced-usage
    topics/voice-calls

.. toctree::
    :hidden:
    :caption: Meta

    faq
    glossary
    powered-by
    support-pyrogram
    license
    releases/index

.. toctree::
    :hidden:
    :caption: Telegram API

    telegram/functions/index
    telegram/types/index

.. raw:: html

    <div align="center">
        <a href="/">
            <div><img src="_static/pyrogram.png" alt="Pyrogram Logo" width="420"></div>
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
        message.reply_text("Hello {}".format(message.from_user.first_name))


    app.run()

**Pyrogram** is an elegant, easy-to-use Telegram_ client library and framework written from the ground up in Python and
C. It enables you to easily create custom apps for both user and bot identities (bot API alternative) via the
:doc:`MTProto API <topics/mtproto-vs-botapi>`.

.. _Telegram: https://telegram.org

How the Documentation is Organized
----------------------------------

Contents are organized into self-contained topics and can be all accessed from the sidebar, or by following them in
order using the :guilabel:`Next` button at the end of each page. Here below you can, instead, find a list of the most
relevant pages for a quick access.

First Steps
^^^^^^^^^^^

.. hlist::
    :columns: 2

    - :doc:`Quick Start <intro/quickstart>`: Overview to get you started quickly.
    - :doc:`Calling Methods <start/invoking>`: How to call Pyrogram's methods.
    - :doc:`Handling Updates <start/updates>`: How to handle Telegram updates.
    - :doc:`Error Handling <start/errors>`: How to handle API errors correctly.

API Reference
^^^^^^^^^^^^^

.. hlist::
    :columns: 2

    - :doc:`Pyrogram Client <api/client>`: Reference details about the Client class.
    - :doc:`Available Methods <api/methods/index>`: List of available high-level methods.
    - :doc:`Available Types <api/types/index>`: List of available high-level types.
    - :doc:`Bound Methods <api/bound-methods/index>`: List of convenient bound methods.

Meta
^^^^

.. hlist::
    :columns: 2

    - :doc:`Pyrogram FAQ <faq>`: Answers to common Pyrogram questions.
    - :doc:`Pyrogram Glossary <glossary>`: List of words with brief explanations.
    - :doc:`Powered by Pyrogram <powered-by>`: Collection of Pyrogram Projects.
    - :doc:`Support Pyrogram <support-pyrogram>`: Ways to show your appreciation.
    - :doc:`About the License <license>`: Information about the Project license.
    - :doc:`Release Notes <releases/index>`: Release notes for Pyrogram releases.

Last updated on |today|
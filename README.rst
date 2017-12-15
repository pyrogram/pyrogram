|header|

Table of Contents
=================

-   `Overview`_

-   `Requirements`_

    -   `API Keys`_

-   `Installation`_

-   `Getting Started`_

    -   `Setup`_

    -   `Authorization`_

-   `Usage`_

    -   `Simple API Access`_

    -   `Using Raw Functions`_

-   `Development`_

-   `Documentation`_

-   `Contribution`_

-   `Feedback`_

-   `Copyright & License`_


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

API Keys
--------

To obtain an API key:

#.  Visit https://my.telegram.org/apps and log in with your Telegram Account.

#.  Fill out the form to register a new Telegram application.

#.  Done. The Telegram API key consists of two parts: the **App api_id** and
    the **App api_hash**.

**Important:** This key should be kept secret.


Installation
============

You can install and upgrade the library using standard Python tools:

.. code:: shell

    $ pip install --upgrade pyrogram


Getting Started
===============

This section provides all the information you need to start using Pyrogram.
There are a couple of steps you have to follow before you can use the library
to make API calls.

Setup
-----

Create a new ``config.ini`` file at the root of your working directory, paste
the following and replace the **api_id** and **api_hash** values
with `your own`_:

.. code:: ini

    [pyrogram]
    api_id = 12345
    api_hash = 0123456789abcdef0123456789abcdef

Authorization
-------------

Telegram requires that users be authorized in order to use the API.
Pyrogram automatically manages this access, all you need to do is create an
instance of the ``pyrogram.Client`` class and call the ``start`` method:

.. code:: python

    from pyrogram import Client

    client = Client(session_name="example")
    client.start()

This starts an interactive shell asking you to input your **phone number**
(including your `Country Code`_) and the **phone code** you will receive:

.. code::

    Enter phone number: +39**********
    Is "+39**********" correct? (y/n): y
    Enter phone code: 32768


After successfully authorizing yourself, a new file called ``example.session``
will be created allowing Pyrogram executing API calls with your identity.

**Important**: The ``*.session`` file must be kept secret.


Usage
=====

Having `your session`_ created you can now start playing with the API.

Simple API Access
-----------------

The easiest way to interact with the API is via the ``pyrogram.Client`` class
which exposes `bot-like`_ methods. The purpose of this Client class is to make
it **even simpler** to work with Telegram's API by abstracting the raw functions
listed in the API scheme.

The result is a much cleaner interface that allows you to:

-   Get information about the authorized user:

    .. code:: python

        print(client.get_me())

-   Send a message to yourself (Saved Messages):

    .. code:: python

        client.send_message(
            chat_id="me",
            text="Hi there! I'm using Pyrogram"
        )

Using Raw Functions
-------------------

If you want **complete**, low-level access to the Telegram API you have to use
the raw ``functions`` and ``types`` exposed by the ``pyrogram.api`` package and
call any Telegram API method you wish using the ``send`` method provided by the
Client class:

-   Update first name, last name and bio:

    .. code:: python

        from pyrogram.api import functions

        client.send(
            functions.account.UpdateProfile(
                first_name="Dan", last_name="Tès",
                about="Bio written from Pyrogram"
            )
        )

-   Share your Last Seen time only with your contacts:

    .. code:: python

        from pyrogram.api import functions, types

        client.send(
            functions.account.SetPrivacy(
                key=types.InputPrivacyKeyStatusTimestamp(),
                rules=[types.InputPrivacyValueAllowContacts()]
            )
        )

Development
===========

The library is still in its early stages, thus lots of functionalities aiming to
make working with Telegram's API easy are yet to be added.

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

Copyright & License
===================

-   Copyright (C) 2017 Dan Tès <https://github.com/delivrance>

-   Licensed under the terms of the
    `GNU Lesser General Public License v3 or later (LGPLv3+)`_
    

.. _`Telegram Messenger API`: https://core.telegram.org/api#telegram-api

.. _`MTProto Mobile Protocol v2.0`: https://core.telegram.org/mtproto

.. _`Layer 73`: compiler/api/source/main_api.tl

.. _`your own`: `API Keys`_

.. _`Country Code`: https://en.wikipedia.org/wiki/List_of_country_calling_codes

.. _`your session`: `Authorization`_

.. _`bot-like`: https://core.telegram.org/bots/api#available-methods

.. _`Telegram`: https://t.me/joinchat/AWDQ8lK2HgBN7ka4OyWVTw

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
        <br><br>
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

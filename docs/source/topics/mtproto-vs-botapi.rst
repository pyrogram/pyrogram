MTProto vs. Bot API
===================

Pyrogram is a framework written from the ground up that acts as a fully-fledged Telegram client based on the MTProto
API. This means that Pyrogram is able to execute any official client and bot API action and more. This page will
therefore show you why Pyrogram might be a better choice for your project by comparing the two APIs, but first, let's
make it clear what actually is the MTProto and the Bot API.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

What is the MTProto API?
------------------------

`MTProto`_, took alone, is the name of the custom-made, open and encrypted communication protocol created by Telegram
itself --- it's the only protocol used to exchange information between a client and the actual Telegram servers.

The MTProto API on the other hand, is what people for convenience call the main Telegram API in order to distinguish it
from the Bot API. The main Telegram API is able to authorize both users and bots and is built on top of the MTProto
encryption protocol by means of `binary data serialized`_ in a specific way, as described by the `TL language`_, and
delivered using UDP, TCP or even HTTP as transport-layer protocol. Clients that make use of Telegram's main API, such as
Pyrogram, implement all these details.

.. _MTProto: https://core.telegram.org/mtproto
.. _binary data serialized: https://core.telegram.org/mtproto/serialize
.. _TL language: https://core.telegram.org/mtproto/TL

What is the Bot API?
--------------------

The `Bot API`_ is an HTTP(S) interface for building normal bots using a sub-set of the main Telegram API. Bots are
special accounts that are authorized via tokens instead of phone numbers. The Bot API is built yet again on top of the
main Telegram API, but runs on an intermediate server application that in turn communicates with the actual Telegram
servers using MTProto.

.. figure:: //_static/img/mtproto-vs-bot-api.png
    :align: center

.. _Bot API: https://core.telegram.org/bots/api

Advantages of the MTProto API
-----------------------------

Here is a non-exhaustive list of all the advantages in using MTProto-based libraries -- such as Pyrogram -- instead of
the official HTTP Bot API. Using Pyrogram you can:

.. hlist::
    :columns: 1

    - :guilabel:`+` **Authorize both user and bot identities**
    - :guilabel:`--` The Bot API only allows bot accounts

.. hlist::
    :columns: 1

    - :guilabel:`+` **Upload & download any file, up to 2000 MiB each (~2 GB)**
    - :guilabel:`--` The Bot API allows uploads and downloads of files only up to 50 MB / 20 MB in size (respectively).

.. hlist::
    :columns: 1

    - :guilabel:`+` **Has less overhead due to direct connections to Telegram**
    - :guilabel:`--` The Bot API uses an intermediate server to handle HTTP requests before they are sent to the actual
      Telegram servers.

.. hlist::
    :columns: 1

    - :guilabel:`+` **Run multiple sessions at once (for both user and bot identities)**
    - :guilabel:`--` The Bot API intermediate server will terminate any other session in case you try to use the same
      bot again in a parallel connection.

.. hlist::
    :columns: 1

    - :guilabel:`+` **Has much more detailed types and powerful methods**
    - :guilabel:`--` The Bot API types often miss some useful information about Telegram entities and some of the
      methods are limited as well.

.. hlist::
    :columns: 1

    - :guilabel:`+` **Obtain information about any message existing in a chat using their ids**
    - :guilabel:`--` The Bot API simply doesn't support this

.. hlist::
    :columns: 1

    - :guilabel:`+` **Retrieve the whole chat members list of either public or private chats**
    - :guilabel:`--` The Bot API simply doesn't support this

.. hlist::
    :columns: 1

    - :guilabel:`+` **Receive extra updates, such as the one about a user name change**
    - :guilabel:`--` The Bot API simply doesn't support this

.. hlist::
    :columns: 1

    - :guilabel:`+` **Has more meaningful errors in case something went wrong**
    - :guilabel:`--` The Bot API reports less detailed errors

.. hlist::
    :columns: 1

    - :guilabel:`+` **Get API version updates, and thus new features, sooner**
    - :guilabel:`--` The Bot API is simply slower in implementing new features

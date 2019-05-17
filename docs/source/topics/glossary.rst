Pyrogram Glossary
-----------------

This page contains a list of common words with brief explanations related to Pyrogram and, to some extent, Telegram in
general. Some words may as well link to dedicated articles in case the topic is covered in a more detailed fashion.

.. tip::

    If you think something interesting could be added here, feel free to propose it by opening a `Feature Request`_.


.. glossary::

    API
        Application Programming Interface: a set of methods, protocols and tools that make it easier to develop programs
        by providing useful building blocks to the developer.

    API key
        A secret code used to authenticate and/or authorize a specific application to Telegram in order for it to
        control how the API is being used, for example, to prevent abuses of the API.

    DC
        Also known as *data center*, is a place where lots of computer systems are housed and used together in order to
        achieve high quality and availability for services.

    RPC
        Acronym for Remote Procedure call, that is, a function which gets executed at some remote place (i.e. Telegram
        server) and not in your local.

    RPCError
        An error caused by an RPC which must be returned in place of the successful result in order to let the caller
        know something went wrong.

    MTProto
        The name of the custom-made, open encryption protocol by Telegram, implemented in Pyrogram.

    MTProto API
        The Telegram main API Pyrogram makes use of, which is able to connect both users and normal bots to Telegram
        using MTProto as application layer protocol and execute any method Telegram provides from its public schema.

    Bot API
        The `Telegram Bot API`_ that is able to only connect normal bots to Telegram using HTTP as application layer
        protocol and allows to execute a subset of the main Telegram API.

    Pyrogrammer
        A developer that uses Pyrogram to build Telegram applications.

    Userbot
        Also known as *user bot* or *ubot* for short, is a user logged in by third-party Telegram libraries --- such as
        Pyrogram --- to automate some behaviours, like sending messages or reacting to text commands or any other event.

    Session
        Also known as *login session*, is a strictly personal piece of information created and held by both parties
        (client and server) which is used to grant permission into a single account without having to start a new
        authorization process from scratch.

    Callback
        Also known as *callback function*, is a user-defined generic function that *can be* registered to and then
        called-back by the framework when specific events occurs.

    Handler
        An object that wraps around a callback function that is *actually meant* to be registered into the framework,
        which will then be able to handle a specific kind of events, such as a new incoming message, for example.

    Decorator
        Also known as *function decorator*, in Python, is a callable object that is used to modify another function.
        Decorators in Pyrogram are used to automatically register callback functions for `handling updates`_.

.. _Telegram Bot API: https://core.telegram.org/bots/api
.. _handling updates: ../start/updates

.. _Feature Request: https://github.com/pyrogram/pyrogram/issues/new?labels=enhancement&template=feature_request.md

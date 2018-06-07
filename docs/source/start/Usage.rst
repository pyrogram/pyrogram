Usage
=====

Having your `project set up`_ and your account authorized_, it's time to play with the API.
In this section, you'll be shown two ways of communicating with Telegram using Pyrogram. Let's start!

High-level API
--------------

The easiest and recommended way to interact with Telegram is via the high-level Pyrogram methods_ and types_, which are
named after the `Telegram Bot API`_.

.. hint:: If you can't find a method you want to use, chances are it's not implemented yet. In this case, you must use
    the `Raw Functions`_. Meanwhile, feel free to join our Community_ if you're stuck or want to propose a
    new method!

Examples:

-   Get information about the authorized user:

    .. code-block:: python

        print(app.get_me())

-   Send a message to yourself (Saved Messages):

    .. code-block:: python

        app.send_message("me", "Hi there! I'm using Pyrogram")

-   Upload a new photo (with caption):

    .. code-block:: python

        app.send_photo("me", "/home/dan/perla.jpg", "Cute!")

.. _using-raw-functions:

Using Raw Functions
-------------------

If you can't find a high-level method for your needs or want complete, low-level access to the whole Telegram API,
you have to use the raw :mod:`functions <pyrogram.api.functions>` and :mod:`types <pyrogram.api.types>` exposed by the
``pyrogram.api`` package and call any Telegram API method you wish using the :meth:`send() <pyrogram.Client.send>`
method provided by the Client class.

.. hint:: Every high-level method mentioned in the section above is built on top of these raw functions.
    Nothing stops you from using the raw functions only, but they are rather complex and `plenty of them`_ are already
    re-implemented by providing a much simpler and cleaner interface which is very similar to the Bot API.
    If you think a raw function should be wrapped and added as a high-level method, feel free to ask in our Community_!

Examples:

-   Update first name, last name and bio:

    .. code-block:: python

        from pyrogram.api import functions

        ...

        app.send(
            functions.account.UpdateProfile(
                first_name="Dan", last_name="Tès",
                about="Bio written from Pyrogram"
            )
        )

-   Share your Last Seen time only with your contacts:

    .. code-block:: python

        from pyrogram.api import functions, types

        ...

        app.send(
            functions.account.SetPrivacy(
                key=types.InputPrivacyKeyStatusTimestamp(),
                rules=[types.InputPrivacyValueAllowContacts()]
            )
        )

-   Invite users to your channel/supergroup:

    .. code-block:: python

        from pyrogram.api import functions, types

        ...

        app.send(
            functions.channels.InviteToChannel(
                channel=app.resolve_peer(123456789),  # ID or Username
                users=[  # The users you want to invite
                    app.resolve_peer(23456789),  # By ID
                    app.resolve_peer("username"),  # By username
                    app.resolve_peer("393281234567"),  # By phone number
                ]
            )
        )

.. _methods: ../pyrogram/Client.html#available-methods
.. _plenty of them: ../pyrogram/Client.html#available-methods
.. _types: ../pyrogram/types/index.html
.. _Raw Functions: Usage.html#using-raw-functions
.. _Community: https://t.me/PyrogramChat
.. _project set up: Setup.html
.. _authorized: Setup.html#user-authorization
.. _Telegram Bot API: https://core.telegram.org/bots/api
Basic Usage
===========

.. note::

    All the snippets below assume you have successfully created and started a :class:`Client <pyrogram.Client>`
    instance. You also must be authorized, that is, a valid *.session file does exist in your working directory.

Simple API Access
-----------------

The easiest way to interact with the Telegram API is via the :class:`Client <pyrogram.Client>` class, which
exposes bot-like_ methods:

-   Get information about the authorized user:

    .. code-block:: python

        print(app.get_me())

-   Send a message to yourself (Saved Messages):

    .. code-block:: python

        app.send_message("me", "Hi there! I'm using Pyrogram")

-   Upload a new photo (with caption):

    .. code-block:: python

        app.send_photo("me", "/home/dan/perla.jpg", "Cute!")

.. seealso:: For a complete list of the available methods and an exhaustive description for each of them, have a look
    at the :class:`Client <pyrogram.Client>` class.

.. _using-raw-functions:

Using Raw Functions
-------------------

If you want **complete**, low-level access to the Telegram API you have to use the raw
:mod:`functions <pyrogram.api.functions>` and :mod:`types <pyrogram.api.types>` exposed by the ``pyrogram.api``
package and call any Telegram API method you wish using the :meth:`send() <pyrogram.Client.send>` method provided by
the Client class.

Here some examples:

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

.. _bot-like: https://core.telegram.org/bots/api#available-methods
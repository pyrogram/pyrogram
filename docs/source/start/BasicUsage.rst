Basic Usage
===========

.. note::

    All the snippets below assume you have successfully created and started a :obj:`pyrogram.Client` instance.
    You also must be authorized, that is, a valid *.session file does exist in your working directory.

Simple API Access
-----------------

The easiest way to interact with the API is via the :obj:`pyrogram.Client` class which exposes bot-like_ methods.
The purpose of this Client class is to make it even simpler to work with Telegram's API by abstracting the
raw functions listed in the API scheme.

The result is a much cleaner interface that allows you to:

-   Get information about the authorized user:

    .. code-block:: python

        print(client.get_me())

-   Send a message to yourself (Saved Messages):

    .. code-block:: python

        client.send_message(
            chat_id="me",
            text="Hi there! I'm using Pyrogram"
        )

.. seealso:: For a complete list of the available methods have a look at the :obj:`pyrogram.Client` class.

.. _using-raw-functions:

Using Raw Functions
-------------------

If you want **complete**, low-level access to the Telegram API you have to use the raw
:obj:`functions <pyrogram.api.functions>` and :obj:`types <pyrogram.api.types>` exposed by the ``pyrogram.api``
package and call any Telegram API method you wish using the :obj:`send <pyrogram.Client.send>` method provided by
the Client class.

Here some examples:

-   Update first name, last name and bio:

    .. code-block:: python

        from pyrogram.api import functions

        ...

        client.send(
            functions.account.UpdateProfile(
                first_name="Dan", last_name="Tès",
                about="Bio written from Pyrogram"
            )
        )

-   Share your Last Seen time only with your contacts:

    .. code-block:: python

        from pyrogram.api import functions, types

        ...

        client.send(
            functions.account.SetPrivacy(
                key=types.InputPrivacyKeyStatusTimestamp(),
                rules=[types.InputPrivacyValueAllowContacts()]
            )
        )

-   Invite users to your channel/supergroup:

    .. code-block:: python

        from pyrogram.api import functions, types

        ...

        client.send(
            functions.channels.InviteToChannel(
                channel=client.resolve_peer(123456789),  # ID or Username of your channel
                users=[  # The users you want to invite
                    client.resolve_peer(23456789),  # By ID
                    client.resolve_peer("username"),  # By username
                    client.resolve_peer("393281234567"),  # By phone number
                ]
            )
        )

-   Get channel/supergroup participants:

    .. code-block:: python

        import time
        from pyrogram.api import types, functions

        ...

        users = []
        limit = 200
        offset = 0

        while True:
            try:
                participants = client.send(
                    functions.channels.GetParticipants(
                        channel=client.resolve_peer("username"),  # ID or username
                        filter=types.ChannelParticipantsSearch(""),  # Filter by empty string (search for all)
                        offset=offset,
                        limit=limit,
                        hash=0
                    )
                )
            except FloodWait as e:
                # Very large channels will trigger FloodWait.
                # When happens, wait X seconds before continuing
                time.sleep(e.x)
                continue

            if not participants.participants:
                break  # No more participants left

            users.extend(participants.users)
            offset += limit

-   Get history of a chat:

    .. code-block:: python

        import time
        from pyrogram.api import types, functions

        ...

        history = []
        limit = 100
        offset = 0

        while True:
            try:
                messages = client.send(
                    functions.messages.GetHistory(
                        client.resolve_peer("me"),  # Get your own history
                        0, 0, offset, limit, 0, 0, 0
                    )
                )
            except FloodWait as e:
                # For very large histories the method call can raise a FloodWait
                time.sleep(e.x)
                continue

            if not messages.messages:
                break  # No more messages left

            history.extend(messages.messages)
            offset += limit

.. _bot-like: https://core.telegram.org/bots/api#available-methods
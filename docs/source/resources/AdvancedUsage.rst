Advanced Usage
==============

In this section, you'll be shown the alternative way of communicating with Telegram using Pyrogram: the main Telegram
API with its raw functions and types.

Telegram Raw API
----------------

If you can't find a high-level method for your needs or if you want complete, low-level access to the whole
Telegram API, you have to use the raw :mod:`functions <pyrogram.api.functions>` and :mod:`types <pyrogram.api.types>`
exposed by the ``pyrogram.api`` package and call any Telegram API method you wish using the
:meth:`send() <pyrogram.Client.send>` method provided by the Client class.

.. hint::

    Every available high-level method mentioned in the previous page is built on top of these raw functions.

    Nothing stops you from using the raw functions only, but they are rather complex and `plenty of them`_ are already
    re-implemented by providing a much simpler and cleaner interface which is very similar to the Bot API.

    If you think a raw function should be wrapped and added as a high-level method, feel free to ask in our Community_!

Caveats
-------

As hinted before, raw functions and types can be confusing, mainly because people don't realize they must accept
*exactly* the right values, but also because most of them don't have enough Python experience to fully grasp how things
work.

This section will therefore explain some pitfalls to take into consideration when working with the raw API.

Chat IDs
^^^^^^^^

The way Telegram works makes it impossible to directly send a message to a user or a chat by using their IDs only.
Instead, a pair of ``id`` and ``access_hash`` wrapped in a so called ``InputPeer`` is always needed.

There are three different InputPeer types, one for each kind of Telegram entity.
Whenever an InputPeer is needed you must pass one of these:

    - `InputPeerUser <https://docs.pyrogram.ml/types/InputPeerUser>`_ - Users
    - `InputPeerChat <https://docs.pyrogram.ml/types/InputPeerChat>`_ -  Basic Chats
    - `InputPeerChannel <https://docs.pyrogram.ml/types/InputPeerChannel>`_ - Either Channels or Supergroups

But you don't necessarily have to manually instantiate each object because, luckily for you, Pyrogram already provides
:meth:`resolve_peer() <pyrogram.Client.resolve_peer>` as a convenience utility method that returns the correct InputPeer
by accepting a peer ID only.

Another thing to take into consideration about chat IDs is the way they are represented: they are all integers and
all positive within their respective raw types.

Things are different when working with Pyrogram's API because having them in the same space can theoretically lead to
collisions, and that's why Pyrogram (as well as the official Bot API) uses a slightly different representation for each
kind of ID.

For example, given the ID *123456789*, here's how Pyrogram can tell entities apart:

    - ``+ID`` - User: *123456789*
    - ``-ID`` - Chat: *-123456789*
    - ``-100ID`` - Channel (and Supergroup): *-100123456789*

So, every time you take a raw ID, make sure to translate it into the correct ID when you want to use it with an
high-level method.

Examples
--------

-   Update first name, last name and bio:

    .. code-block:: python

        from pyrogram import Client
        from pyrogram.api import functions

        with Client("my_account") as app:
            app.send(
                functions.account.UpdateProfile(
                    first_name="Dan", last_name="Tès",
                    about="Bio written from Pyrogram"
                )
            )

-   Share your Last Seen time only with your contacts:

    .. code-block:: python

        from pyrogram import Client
        from pyrogram.api import functions, types

        with Client("my_account") as app:
            app.send(
                functions.account.SetPrivacy(
                    key=types.InputPrivacyKeyStatusTimestamp(),
                    rules=[types.InputPrivacyValueAllowContacts()]
                )
            )

-   Invite users to your channel/supergroup:

    .. code-block:: python

        from pyrogram import Client
        from pyrogram.api import functions, types

        with Client("my_account") as app:
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
-   Hide Forward Message Headers:

    .. code-block:: python

        from pyrogram import Client
        from pyrogram.api import functions, types

        with Client("my_account") as app:
            app.send(
                functions.account.SetPrivacy(
                    key=types.inputPrivacyKeyForwards(),
                    rules=[types.inputPrivacyValueDisallowAll()]
                )
            )


.. _plenty of them: ../pyrogram/Client.html#messages
.. _Raw Functions: Usage.html#using-raw-functions
.. _Community: https://t.me/PyrogramChat
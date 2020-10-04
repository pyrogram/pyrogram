Advanced Usage
==============

Pyrogram's API, which consists of well documented convenience :doc:`methods <../api/methods/index>` and facade
:doc:`types <../api/types/index>`, exists to provide a much easier interface to the undocumented and often confusing
Telegram API.

In this section, you'll be shown the alternative way of communicating with Telegram using Pyrogram: the main "raw"
Telegram API with its functions and types.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Telegram Raw API
----------------

If you can't find a high-level method for your needs or if you want complete, low-level access to the whole
Telegram API, you have to use the raw :mod:`~pyrogram.raw.functions` and :mod:`~pyrogram.raw.types`.

As already hinted, raw functions and types can be really confusing, mainly because people don't realize soon enough they
accept *only* the right types and that all required parameters must be filled in. This section will therefore explain
some pitfalls to take into consideration when working with the raw API.

.. hint::

    Every available high-level methods in Pyrogram is built on top of these raw functions.

    Nothing stops you from using the raw functions only, but they are rather complex and
    :doc:`plenty of them <../api/methods/index>` are already re-implemented by providing a much simpler and cleaner
    interface which is very similar to the Bot API (yet much more powerful).

    If you think a raw function should be wrapped and added as a high-level method, feel free to ask in our Community_!

Invoking Functions
^^^^^^^^^^^^^^^^^^

Unlike the :doc:`methods <../api/methods/index>` found in Pyrogram's API, which can be called in the usual simple way,
functions to be invoked from the raw Telegram API have a different way of usage and are more complex.

First of all, both :doc:`raw functions <../telegram/functions/index>` and :doc:`raw types <../telegram/types/index>`
live in their respective packages (and sub-packages): ``pyrogram.raw.functions``, ``pyrogram.raw.types``. They all exist
as Python classes, meaning you need to create an instance of each every time you need them and fill them in with the
correct values using named arguments.

Next, to actually invoke the raw function you have to use the :meth:`~pyrogram.Client.send` method provided by the
Client class and pass the function object you created.

Here's some examples:

-   Update first name, last name and bio:

    .. code-block:: python

        from pyrogram import Client
        from pyrogram.raw import functions

        with Client("my_account") as app:
            app.send(
                functions.account.UpdateProfile(
                    first_name="Dan", last_name="Tès",
                    about="Bio written from Pyrogram"
                )
            )

-   Disable links to your account when someone forwards your messages:

    .. code-block:: python

        from pyrogram import Client
        from pyrogram.raw import functions, types

        with Client("my_account") as app:
            app.send(
                functions.account.SetPrivacy(
                    key=types.PrivacyKeyForwards(),
                    rules=[types.InputPrivacyValueDisallowAll()]
                )
            )

-   Invite users to your channel/supergroup:

    .. code-block:: python

        from pyrogram import Client
        from pyrogram.raw import functions, types

        with Client("my_account") as app:
            app.send(
                functions.channels.InviteToChannel(
                    channel=app.resolve_peer(123456789),  # ID or Username
                    users=[  # The users you want to invite
                        app.resolve_peer(23456789),  # By ID
                        app.resolve_peer("username"),  # By username
                        app.resolve_peer("+393281234567"),  # By phone number
                    ]
                )
            )

Chat IDs
^^^^^^^^

The way Telegram works makes it impossible to directly send a message to a user or a chat by using their IDs only.
Instead, a pair of ``id`` and ``access_hash`` wrapped in a so called ``InputPeer`` is always needed. Pyrogram allows
sending messages with IDs only thanks to cached access hashes.

There are three different InputPeer types, one for each kind of Telegram entity.
Whenever an InputPeer is needed you must pass one of these:

- :class:`~pyrogram.raw.types.InputPeerUser` - Users
- :class:`~pyrogram.raw.types.InputPeerChat` -  Basic Chats
- :class:`~pyrogram.raw.types.InputPeerChannel` - Either Channels or Supergroups

But you don't necessarily have to manually instantiate each object because, luckily for you, Pyrogram already provides
:meth:`~pyrogram.Client.resolve_peer` as a convenience utility method that returns the correct InputPeer
by accepting a peer ID only.

Another thing to take into consideration about chat IDs is the way they are represented: they are all integers and
all positive within their respective raw types.

Things are different when working with Pyrogram's API because having them in the same space can theoretically lead to
collisions, and that's why Pyrogram (as well as the official Bot API) uses a slightly different representation for each
kind of ID.

For example, given the ID *123456789*, here's how Pyrogram can tell entities apart:

- ``+ID`` User: *123456789*
- ``-ID`` Chat: *-123456789*
- ``-100ID`` Channel or Supergroup: *-100123456789*

So, every time you take a raw ID, make sure to translate it into the correct ID when you want to use it with an
high-level method.

.. _Community: https://t.me/Pyrogram
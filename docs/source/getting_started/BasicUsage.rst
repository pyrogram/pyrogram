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

        client.send(
            functions.account.UpdateProfile(
                first_name="Dan", last_name="Tès",
                about="Bio written from Pyrogram"
            )
        )

-   Share your Last Seen time only with your contacts:

    .. code-block:: python

        from pyrogram.api import functions, types

        client.send(
            functions.account.SetPrivacy(
                key=types.InputPrivacyKeyStatusTimestamp(),
                rules=[types.InputPrivacyValueAllowContacts()]
            )
        )

.. _bot-like: https://core.telegram.org/bots/api#available-methods
MTProto vs. Bot API
===================

Being Pyrogram an MTProto-based library, this very feature makes it already superior to, what is usually called, the
official Bot API.

What is the MTProto API?
------------------------

MTProto, took alone, is the name of the custom-made, open and encrypted communication protocol created by Telegram
itself --- it's the only protocol used to exchange information between a client application and the actual Telegram
servers.

The MTProto **API** however, is what people, for convenience, call the main Telegram API as a whole. This API is able
to authorize both users and bots and happens to be built on top of the MTProto encryption protocol by means of binary
data serialized in a specific way, as described by the TL language, hence the correlation.

What is the Bot API?
--------------------

The Bot API is an HTTP(S) interface for building normal bots. Bots are special accounts that are authorized via tokens
instead of phone numbers. The Bot API is built yet again on top of the main Telegram API, but runs on an intermediate
server application that in turn communicates with the actual Telegram servers using MTProto.

.. figure:: https://i.imgur.com/C108qkX.png
    :align: center

Advantages of the MTProto API
-----------------------------

Here is a list of all the known advantages in using MTProto-based libraries (such as Pyrogram) instead of the official
HTTP Bot API. Using Pyrogram you can:

- **Authorize both user and bot identities**: The Bot API only allows bot accounts.

- **Upload & download any file, up to 1500 MB each (~1.5 GB)**: The Bot API allows uploads and downloads of files only
  up to 50 MB / 20 MB in size (respectively).

- **Has less overhead due to direct connections to Telegram**: The Bot API uses an intermediate server to handle HTTP
  requests before they are sent to the actual Telegram servers.

- **Run multiple sessions at once, up to 10 per account (either bot or user)**: The Bot API intermediate server will
  terminate any other session in case you try to use the same bot again in a parallel connection.

- **Get information about any public chat by usernames, even if not a member**: The Bot API simply doesn't support this.

- **Obtain information about any message existing in a chat using their ids**: The Bot API simply doesn't support this.

- **Retrieve the whole chat members list of either public or private chats**: The Bot API simply doesn't support this.

- **Receive extra updates, such as the one about a user name change**: The Bot API simply doesn't support this.

- **Has more meaningful errors in case something went wrong**: The Bot API reports less detailed errors.

- **Has much more detailed types and powerful methods**: The Bot API types often miss some useful information about
  Telegram's type and some of the methods are limited as well.

- **Get API version updates, and thus new features, sooner**: The Bot API is simply slower in implementing new features.
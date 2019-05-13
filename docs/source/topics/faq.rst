Pyrogram FAQ
============

This FAQ page provides answers to common questions about Pyrogram and, to some extent, Telegram in general.

.. contents:: Contents
    :backlinks: none
    :local:

What is Pyrogram?
-----------------

**Pyrogram** is an elegant, easy-to-use Telegram_ client library and framework written from the ground up in Python and
C. It enables you to easily create custom applications for both user and bot identities (bot API alternative) via the
`MTProto API`_ with the Python programming language.

.. _Telegram: https://telegram.org
.. _MTProto API: https://core.telegram.org/api#telegram-api

What does "Pyrogram" mean?
--------------------------

The word "Pyrogram" is composed by **pyro**, which comes from the Greek word *πῦρ (pyr)*, meaning fire, and **gram**,
from *Telegram*. The word *pyro* itself is built from *Python*, **py** for short, and the suffix **ro** to come up with
the word *fire*, which also inspired the project logo.

How old is Pyrogram?
--------------------

Pyrogram was first released on December 12, 2017. The actual work on the framework began roughly three months prior the
initial public release on `GitHub`_.

.. _GitHub: https://github.com/pyrogram/pyrogram

Why do I need an API key for bots?
----------------------------------

Requests against the official bot API endpoint are made via JSON/HTTP, but are handled by a backend application that
implements the MTProto protocol -- just like Pyrogram -- and uses its own API key, which is always required, but hidden
to the public.

.. figure:: https://i.imgur.com/C108qkX.png
    :align: center

Using MTProto is the only way to communicate with the actual Telegram servers, and the main API requires developers to
identify applications by means of a unique key; the bot token identifies a bot as a user and replaces the user's phone
number only.

I started a client but nothing happens!
---------------------------------------

If you are connecting from Russia, China or Iran `you need a proxy`_, because Telegram could be partially or
totally blocked in those countries.

Another possible cause might be network issues, either yours or Telegram's. To confirm this, add the following code on
the top of your script and run it again. You should see some error mentioning a socket timeout or an unreachable network
in a bunch of seconds:

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.INFO)

|bug report|

.. _you need a proxy: proxy

I keep getting [400 PEER_ID_INVALID] error!
-------------------------------------------

The error in question is **[400 PEER_ID_INVALID]: The id/access_hash combination is invalid**, and could mean several
things:

- The chat id you tried to use is simply wrong, double check it.
- The chat id refers to a group or channel you are not a member of.
- The chat id refers to a user you have't seen yet (from contacts, groups in common, forwarded messages or private
  chats).

|bug report|

.. |bug report| replace::

    **Note:** If you really believe this should not happen, kindly open a `Bug Report`_.

.. _Bug Report: https://github.com/pyrogram/pyrogram/issues/new?labels=bug&template=bug_report.md

My account has been deactivated/limited!
----------------------------------------

First of all, you should understand that Telegram wants to be a safe place for people to stay in, and to pursue this
goal there are automatic protection systems running to prevent flood and spam, as well as a moderation team of humans
who reviews reports.

**Pyrogram is a tool at your commands; it only does what you tell it to do, the rest is up to you.**

Having said that, here's how a list of what Telegram definitely doesn't like:

- Flood, abusing the API.
- Spam, sending unsolicited messages or adding people to unwanted groups and channels.
- Virtual/VoIP and cheap real numbers, because they are relatively easy to get and likely used for spam/flood.

However, you might be right, and your account was deactivated/limited without any reason. This could happen because of
mistakes by either the automatic systems or a moderator. In such cases you can kindly email Telegram at
recover@telegram.org, contact `@smstelegram`_ on Twitter or use `this form`_.

.. _@smstelegram: https://twitter.com/smstelegram
.. _this form: https://telegram.org/support
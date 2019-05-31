Pyrogram FAQ
============

This FAQ page provides answers to common questions about Pyrogram and, to some extent, Telegram in general.

.. tip::

    If you think something interesting could be added here, feel free to propose it by opening a `Feature Request`_.

.. contents:: Contents
    :backlinks: none
    :local:
    :depth: 1

What is Pyrogram?
-----------------

**Pyrogram** is an elegant, easy-to-use Telegram_ client library and framework written from the ground up in Python and
C. It enables you to easily create custom applications for both user and bot identities (bot API alternative) via the
:doc:`MTProto API <topics/mtproto-vs-botapi>` with the Python programming language.

.. _Telegram: https://telegram.org

Where does the name come from?
------------------------------

The name "Pyrogram" is composed by **pyro**, which comes from the Greek word *πῦρ (pyr)*, meaning fire, and **gram**,
from *Telegram*. The word *pyro* itself is built from *Python*, **py** for short, and the suffix **ro** to come up with
the word *fire*, which also inspired the project logo.

How old is Pyrogram?
--------------------

Pyrogram was first released on December 12, 2017. The actual work on the framework began roughly three months prior the
initial public release on `GitHub`_.

.. _GitHub: https://github.com/pyrogram/pyrogram

Why Pyrogram?
-------------

- **Easy**: You can install Pyrogram with pip and start building your applications right away.
- **Elegant**: Low-level details are abstracted and re-presented in a much nicer and easier way.
- **Fast**: Crypto parts are boosted up by TgCrypto_, a high-performance library written in pure C.
- **Documented**: Pyrogram API methods, types and public interfaces are well documented.
- **Type-hinted**: Exposed Pyrogram types and method parameters are all type-hinted.
- **Updated**, to make use of the latest Telegram API version and features.
- **Bot API-like**: Similar to the Bot API in its simplicity, but much more powerful and detailed.
- **Pluggable**: The :doc:`Smart Plugin <topics/smart-plugins>` system allows to write components with minimal
  boilerplate code.
- **Comprehensive**: Execute any :doc:`advanced action <topics/advanced-usage>` an official client is able to do, and
  even more.

.. _TgCrypto: https://github.com/pyrogram/tgcrypto

What can MTProto do more than the Bot API?
------------------------------------------

For a detailed answer, please refer to the :doc:`MTProto vs. Bot API <topics/mtproto-vs-botapi>` page.

Why do I need an API key for bots?
----------------------------------

Requests against the official bot API endpoint are made via JSON/HTTP, but are handled by an intermediate server
application that implements the MTProto protocol -- just like Pyrogram -- and uses its own API key, which is always
required, but hidden to the public.

.. figure:: https://i.imgur.com/C108qkX.png
    :align: center

Using MTProto is the only way to communicate with the actual Telegram servers, and the main API requires developers to
identify applications by means of a unique key; the bot token identifies a bot as a user and replaces the user's phone
number only.

Can I use the same file_id across different accounts?
-----------------------------------------------------

No, Telegram doesn't allow this.

File ids are personal and bound to a specific user/bot -- and an attempt in using a foreign file id will result in
errors such as ``[400 MEDIA_EMPTY]``.

The only exception are stickers' file ids; you can use them across different accounts without any problem, like this
one: ``CAADBAADyg4AAvLQYAEYD4F7vcZ43AI``.

Can I use Bot API's file_ids in Pyrogram?
-----------------------------------------

Definitely! All file ids you might have taken from the Bot API are 100% compatible and re-usable in Pyrogram...

...at least for now.

Telegram is slowly changing some server's internals and it's doing it in such a way that file ids are going to break
inevitably. Not only this, but it seems that the new, hypothetical, file ids could also possibly expire at anytime, thus
losing the *persistence* feature.

This change will most likely affect the official :doc:`Bot API <topics/mtproto-vs-botapi>` too (unless Telegram
implements some workarounds server-side to keep backwards compatibility, which Pyrogram could in turn make use of) and
we can expect a proper notice from Telegram.

Can I use multiple clients at once on the same account?
-------------------------------------------------------

Yes, you can. Both user and bot accounts are able to run multiple sessions in parallel (up to 10 per account). However,
you must pay attention and not use the *same* exact session in more than one client at the same time. In other words:

- Avoid copying your session file: even if you rename the file, the copied sessions will still point to a specific one
  stored in the server.

- Make sure that only one instance of your script runs, using your session file.

If you -- even accidentally -- fail to do so, all the previous session copies will immediately stop receiving updates
and eventually the server will start throwing the error ``[406 AUTH_KEY_DUPLICATED]``, inviting you to login again.

Why is that so? Because the server has recognized two identical sessions are running in two different locations, and
concludes it could possibly be due to a cloned/stolen device. Having the session ended in such occasions will protect
the user's privacy.

So, the only correct way to run multiple clients on the same account is authorizing your account (either user or bot)
from the beginning every time, and use one separate session for each parallel client you are going to use.

I started a client and nothing happens!
---------------------------------------

If you are connecting from Russia, China or Iran :doc:`you need a proxy <topics/proxy>`, because Telegram could be
partially or totally blocked in those countries.

Another possible cause might be network issues, either yours or Telegram's. To confirm this, add the following code on
the top of your script and run it again. You should see some error mentioning a socket timeout or an unreachable network
in a bunch of seconds:

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.INFO)

Another way to confirm you aren't able to connect to Telegram is by pinging these IP addresses and see whether ping
fails or not:

- DC1: ``149.154.175.50``
- DC2: ``149.154.167.51``
- DC3: ``149.154.175.100``
- DC4: ``149.154.167.91``
- DC5: ``91.108.56.149``

I keep getting PEER_ID_INVALID error!
-------------------------------------------

The error in question is ``[400 PEER_ID_INVALID]``, and could mean several
things:

- The chat id you tried to use is simply wrong, double check it.
- The chat id refers to a group or channel you are not a member of.
- The chat id refers to a user you have't seen yet (from contacts, groups in common, forwarded messages or private
  chats).
- The chat id argument you passed is in form of a string; you have to convert it into an integer with ``int(chat_id)``.

My verification code expires immediately!
-----------------------------------------

That is because you likely shared it across any of your Telegram chats. Yes, that's right: the server keeps scanning the
messages you send and if an active verification code is found it will immediately expire, automatically.

The reason behind this is to protect unaware users from giving their account access to any potential scammer, but if you
legitimately want to share your account(s) verification codes, consider scrambling them, e.g. ``12345`` → ``1-2-3-4-5``.

My account has been deactivated/limited!
----------------------------------------

First of all, you should understand that Telegram wants to be a safe place for people to stay in, and to pursue this
goal there are automatic protection systems running to prevent flood and spam, as well as a moderation team of humans
who review reports.

.. centered:: Pyrogram is a tool at your commands; it only does what you tell it to do, the rest is up to you.

Having said that, here's a list of what Telegram definitely doesn't like:

- Flood, abusing the API.
- Spam, sending unsolicited messages or adding people to unwanted groups and channels.
- Virtual/VoIP and cheap real numbers, because they are relatively easy to get and likely used for spam/flood.

However, you might be right, and your account was deactivated/limited without any reason. This could happen because of
mistakes by either the automatic systems or a moderator. In such cases you can kindly email Telegram at
recover@telegram.org, contact `@smstelegram`_ on Twitter or use `this form`_.

.. _@smstelegram: https://twitter.com/smstelegram
.. _this form: https://telegram.org/support

.. _Bug Report: https://github.com/pyrogram/pyrogram/issues/new?labels=bug&template=bug_report.md
.. _Feature Request: https://github.com/pyrogram/pyrogram/issues/new?labels=enhancement&template=feature_request.md

Pyrogram FAQ
============

.. role:: strike
    :class: strike

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

How stable and reliable is Pyrogram?
------------------------------------

So far, since its first public release, Pyrogram has always shown itself to be quite reliable in handling client-server
interconnections and just as stable when keeping long running applications online. The only annoying issues faced are
actually coming from Telegram servers internal errors and down times, from which Pyrogram is able to recover itself
automatically.

To challenge the framework, the creator is constantly keeping a public
`welcome bot <https://github.com/pyrogram/pyrogram/blob/develop/examples/welcomebot.py>`_ online 24/7 on his own,
relatively-busy account for well over a year now.

In addition to that, about six months ago, one of the most popular Telegram bot has been rewritten from scratch
:doc:`using Pyrogram <powered-by>` and is serving more than 200,000 Monthly Active Users since
then, uninterruptedly and without any need for restarting it.

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

:strike:`Definitely! All file ids you might have taken from the Bot API are 100% compatible and re-usable in Pyrogram.`

Starting from :doc:`Pyrogram v0.14.1 (Layer 100) <releases/v0.14.1>`, the file_id format of all photo-like objects has
changed. Types affected are: :obj:`~pyrogram.Thumbnail`, :obj:`~pyrogram.ChatPhoto` and :obj:`~pyrogram.Photo`. Any
other file id remains compatible with the Bot API.

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
concludes it could possibly be due to a cloned/stolen device. Having the session terminated in such occasions will
protect the user's privacy.

So, the only correct way to run multiple clients on the same account is authorizing your account (either user or bot)
from the beginning every time, and use one separate session for each parallel client you are going to use.

I started a client and nothing happens!
---------------------------------------

If you are connecting from Russia, China or Iran :doc:`you need a proxy <topics/proxy>`, because Telegram could be
partially or totally blocked in those countries. More information about this block can be found at
`Wikipedia <https://en.wikipedia.org/wiki/Blocking_Telegram_in_Russia>`_.

Another possible cause might be network issues, either yours or Telegram's. To confirm this, add the following code on
the top of your script and run it again. You should see some error mentioning a socket timeout or an unreachable network
in a bunch of seconds:

.. code-block:: python

    import logging
    logging.basicConfig(level=logging.INFO)

Another way to confirm you aren't able to connect to Telegram is by pinging the IP addresses below and see whether ping
fails or not.

What are the IP addresses of Telegram Data Centers?
---------------------------------------------------

The Telegram cloud is currently composed by a decentralized, multi-DC infrastructure (currently 5 DCs, each of which can
work independently) spread in different locations worldwide. However, some of the less busy DCs have been lately
dismissed and their IP addresses are now kept as aliases to the nearest one.

.. csv-table:: Production Environment
    :header: ID, Location, IPv4, IPv6
    :widths: auto
    :align: center

    DC1, "MIA, Miami FL, USA", ``149.154.175.53``, ``2001:b28:f23d:f001::a``
    DC2, "AMS, Amsterdam, NL", ``149.154.167.51``, ``2001:67c:4e8:f002::a``
    DC3*, "MIA, Miami FL, USA", ``149.154.175.100``, ``2001:b28:f23d:f003::a``
    DC4, "AMS, Amsterdam, NL", ``149.154.167.91``, ``2001:67c:4e8:f004::a``
    DC5, "SIN, Singapore, SG", ``91.108.56.130``, ``2001:b28:f23f:f005::a``

.. csv-table:: Test Environment
    :header: ID, Location, IPv4, IPv6
    :widths: auto
    :align: center

    DC1, "MIA, Miami FL, USA", ``149.154.175.10``, ``2001:b28:f23d:f001::e``
    DC2, "AMS, Amsterdam, NL", ``149.154.167.40``, ``2001:67c:4e8:f002::e``
    DC3*, "MIA, Miami FL, USA", ``149.154.175.117``, ``2001:b28:f23d:f003::e``

.. centered:: More info about the Test Environment can be found :doc:`here <topics/test-servers>`.

***** Alias DC

Thanks to `@FrayxRulez <https://t.me/tgbetachat/104921>`_ for telling about alias DCs.

I want to migrate my account from DCX to DCY.
---------------------------------------------

This question is often asked by people who find their account(s) always being connected to DC1 - USA (for example), but
are connecting from a place far away (e.g DC4 - Europe), thus resulting in slower interactions when using the API
because of the great physical distance between the user and its associated DC.

When registering an account for the first time, is up to Telegram to decide which DC the new user is going to be created
in, based on the phone number origin.

Even though Telegram `documentations <https://core.telegram.org/api/datacenter#user-migration>`_ state the server might
decide to automatically migrate a user in case of prolonged usages from a distant, unusual location and albeit this
mechanism is also `confirmed <https://twitter.com/telegram/status/427131446655197184>`_ to exist by Telegram itself,
it's currently not possible to have your account migrated, in any way, simply because the feature was once planned but
not yet implemented.

Thanks to `@gabriel <https://t.me/AnotherGroup/217699>`_ for confirming the feature was not implemented yet.

Why is my client reacting slowly in supergroups?
------------------------------------------------

This issue affects only some supergroups or only some members within the same supergroup. Mostly, it affects supergroups
whose creator's account (and thus the supergroup itself) lives inside a **different DC**, far away from yours, but could
also depend on where a member is connecting from.

Because of how Telegram works internally, every single message you receive from and send to other members must pass
through the creator's DC, and in the worst case where you, the creator and another member all belong to three different
DCs, the other member messages have to go through from its DC to the creator's DC and finally to your DC. This process
will inevitably take its time.

    To confirm this theory and see it by yourself, you can test in a supergroup where you are sure all parties live
    inside the same DC. In this case the responses will be faster.

Another reason that makes responses come slowly is that messages are **dispatched by priority**. Depending on the kind
of member, some users receive messages faster than others and for big and busy supergroups the delay might become
noticeable, especially if you are among the lower end of the priority list:

1. Creator.
2. Administrators.
3. Bots.
4. Mentioned users.
5. Recent online users.
6. Everyone else.

Thanks to `@Manuel15 <https://t.me/PyrogramChat/76990>`_ for the priority list.

I keep getting PEER_ID_INVALID error!
-------------------------------------

The error in question is ``[400 PEER_ID_INVALID]``, and could mean several things:

- The chat id you tried to use is simply wrong, double check it.
- The chat id refers to a group or channel you are not a member of.
- The chat id argument you passed is in form of a string; you have to convert it into an integer with ``int(chat_id)``.
- The chat id refers to a user your current session haven't met yet.

About the last point: in order for you to meet a user and thus communicate with them, you should ask yourself how to
contact people using official apps. The answer is the same for Pyrogram too and involves normal usages such as searching
for usernames, meet them in a common group, have their phone contacts saved, getting a message mentioning them (either a
forward or a mention in the message text).

UnicodeEncodeError: '<encoding>' codec can't encode …
-----------------------------------------------------

Where ``<encoding>`` might be *ascii*, *cp932*, *charmap* or anything else other than **utf-8**. This error usually
shows up when you try to print something and has very little to do with Pyrogram itself as it is strictly related to
your own terminal. To fix it, either find a way to change the encoding settings of your terminal to UTF-8 or switch to a
better terminal altogether.

Uploading with URLs gives error WEBPAGE_CURL_FAILED
---------------------------------------------------

When uploading media files using an URL, the server automatically tries to download the media and uploads it to the
Telegram cloud. This error usually happens in case the provided URL is not publicly accessible by Telegram itself or the
media exceeds 20 MB in size. In such cases, your only option is to download the media yourself and upload from your
local machine.

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

And thanks to `@koteeq <https://t.me/koteeq>`_, here's a good explanation of how, probably, the system works:

.. raw:: html

    <script
        async src="https://telegram.org/js/telegram-widget.js?5"
        data-telegram-post="PyrogramChat/69424"
        data-width="100%">
    </script>
    <br><br>

However, you might be right, and your account was deactivated/limited without any good reason. This could happen because
of mistakes by either the automatic systems or a moderator. In such cases you can kindly email Telegram at
recover@telegram.org, contact `@smstelegram`_ on Twitter or use `this form`_.

Are there any secret easter eggs?
---------------------------------

Yes. If you found one, `let me know`_!

.. _let me know: https://t.me/pyrogram

.. _@smstelegram: https://twitter.com/smstelegram
.. _this form: https://telegram.org/support

.. _Bug Report: https://github.com/pyrogram/pyrogram/issues/new?labels=bug&template=bug_report.md
.. _Feature Request: https://github.com/pyrogram/pyrogram/issues/new?labels=enhancement&template=feature_request.md

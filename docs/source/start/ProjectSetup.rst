Project Setup
=============

This section provides all the information you need to setup your project with Pyrogram.
There are a few steps you have to follow before you can actually use the library to make API calls.

API Keys
--------

The very first step requires you to obtain a valid Telegram API key.
If you already have one you can skip this, otherwise:

#. Visit https://my.telegram.org/apps and log in with your Telegram Account.
#. Fill out the form to register a new Telegram application.
#. Done. The Telegram API key consists of two parts: the **App api_id** and the **App api_hash**

.. important:: This key should be kept secret.

Configuration
-------------

Create a new ``config.ini`` file at the root of your working directory,
copy-paste the following and replace the **api_id** and **api_hash** values with `your own <#api-keys>`_:

.. code-block:: ini

    [pyrogram]
    api_id = 12345
    api_hash = 0123456789abcdef0123456789abcdef

Authorization
-------------

Telegram requires that users be authorized in order to use the API.
Pyrogram automatically manages this access, all you need to do is create an instance of
the :class:`pyrogram.Client` class by passing to it a ``<session_name>`` of your choice
and call the :obj:`start <pyrogram.Client.start>` method:

.. code-block:: python

    from pyrogram import Client

    client = Client(session_name="example")
    client.start()

This starts an interactive shell asking you to input your **phone number** (including your `Country Code`_)
and the **phone code** you will receive:

.. code::

    Enter phone number: +39**********
    Is "+39**********" correct? (y/n): y
    Enter phone code: 32768

After successfully authorizing yourself, a new file called ``example.session`` will be created allowing
Pyrogram executing API calls with your identity.

.. important:: Your *.session file(s) must be kept secret.

.. note::

    The authorization process is executed only once.
    However, the code above is always required; as long as a valid session file exists,
    Pyrogram will use that and won't ask you to enter your phone number again when you restart your script.

.. _`Country Code`: https://en.wikipedia.org/wiki/List_of_country_calling_codes
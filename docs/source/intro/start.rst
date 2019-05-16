Quick Start
===========

The next few steps serve as a quick start for all new Pyrogrammers that want to get something done as fast as possible!

Get Pyrogram Real Fast
----------------------

1. Install Pyrogram with ``pip3 install -U pyrogram``.

2. Get your own Telegram API key from https://my.telegram.org/apps.

3.  Open your best text editor and paste the following:

    .. code-block:: python

        from pyrogram import Client

        api_id = 12345
        api_hash = "0123456789abcdef0123456789abcdef"

        with Client("my_account", api_id, api_hash) as app:
            app.send_message("me", "Greetings from **Pyrogram**!")

4. Replace *api_id* and *api_hash* values with your own.

5. Save the file as ``pyro.py``.

6. Run the script with ``python3 pyro.py``

7. Follow the instructions on your terminal to login.

8. Watch Pyrogram send a message to yourself.

9. Join our `community`_.

10. Say, "hi!".

Enjoy the API
-------------

That was just a quick overview that barely scratched the surface!
In the next few pages of the introduction, we'll take a much more in-depth look of what we have just done above.

Feeling eager to continue? You can take a shortcut to `Calling Methods`_ and come back later to learn some more details.

.. _community: //t.me/pyrogramchat
.. _Calling Methods: ../start/invoking
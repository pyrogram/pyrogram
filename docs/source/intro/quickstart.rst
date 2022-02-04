Quick Start
===========

The next few steps serve as a quick start to see Pyrogram in action as fast as possible.

Get Pyrogram Real Fast
----------------------

.. admonition :: Cloud Credits
    :class: tip

    If you need a cloud server to host your applications, try Hetzner Cloud. You can sign up with
    `this link <https://hetzner.cloud/?ref=9CyT92gZEINU>`_ to get €20 in cloud credits.

1. Install Pyrogram with ``pip3 install -U pyrogram``.

2. Get your own Telegram API key from https://my.telegram.org/apps.

3.  Open the text editor of your choice and paste the following:

    .. code-block:: python

        import asyncio
        from pyrogram import Client

        api_id = 12345
        api_hash = "0123456789abcdef0123456789abcdef"

        async def main():
            async with Client("my_account", api_id, api_hash) as app:
                await app.send_message("me", "Greetings from **Pyrogram**!")

        asyncio.run(main())

4. Replace *api_id* and *api_hash* values with your own.

5. Save the file as ``hello.py``.

6. Run the script with ``python3 hello.py``

7. Follow the instructions on your terminal to login.

8. Watch Pyrogram send a message to yourself.

Enjoy the API
-------------

That was just a quick overview. In the next few pages of the introduction, we'll take a much more in-depth look of what
we have just done above.

If you are feeling eager to continue you can take a shortcut to :doc:`Calling Methods <../start/invoking>` and come back
later to learn some more details.

.. _community: https://t.me/Pyrogram

Synchronous Usage
=================

Pyrogram is an asynchronous framework and as such it is subject to the asynchronous rules. It can, however, run in
synchronous mode (also known as non-asynchronous or sync/non-async for short). This mode exists mainly as a convenience
way for invoking methods without the need of ``async``/``await`` keywords and the extra boilerplate, but **it's not the
intended way to use the framework**.

You can use Pyrogram in this synchronous mode when you want to write something short and contained without the
async boilerplate or in case you want to combine Pyrogram with other libraries that are not async.

.. warning::

    You have to be very careful when using the framework in its synchronous, non-native form, especially when combined
    with other non-async libraries because thread blocking operations that clog the asynchronous event loop underneath
    will make the program run erratically.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Synchronous Invocations
-----------------------

The following is a standard example of running asynchronous functions with Python's asyncio.
Pyrogram is being used inside the main function with its asynchronous interface.

.. code-block:: python

    import asyncio
    from pyrogram import Client


    async def main():
        app = Client("my_account")

        async with app:
            await app.send_message("me", "Hi!")


    asyncio.run(main())

To run Pyrogram synchronously, use the non-async context manager as shown in the following example.
As you can see, the non-async example becomes less cluttered.

.. code-block:: python

    from pyrogram import Client

    app = Client("my_account")

    with app:
        app.send_message("me", "Hi!")

Synchronous handlers
--------------------

You can also have synchronous handlers; you only need to define the callback function without using ``async def`` and
invoke API methods by not placing ``await`` in front of them. Mixing ``def`` and ``async def`` handlers together is also
possible.

.. code-block:: python

    @app.on_message()
    async def handler1(client, message):
        await message.forward("me")

    @app.on_edited_message()
    def handler2(client, message):
        message.forward("me")

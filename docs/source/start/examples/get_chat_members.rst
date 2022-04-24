get_chat_members
================

This example shows how to get all the members of a chat.

.. code-block:: python

    from pyrogram import Client

    # Target channel/supergroup
    TARGET = -100123456789

    app = Client("my_account")


    async def main():
        async with app:
            async for member in app.get_chat_members(TARGET):
                print(member)


    app.run(main())
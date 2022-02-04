Scheduling Tasks
================

Scheduling tasks means executing one or more functions periodically at pre-defined intervals or after a delay. This is
useful, for example, to send recurring messages to specific chats or users.

This page will show examples on how to integrate Pyrogram with ``apscheduler`` in both asynchronous and
non-asynchronous contexts. For more detailed information, you can visit and learn from the library documentation.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Using apscheduler
-----------------

- Install with ``pip3 install apscheduler``
- Documentation: https://apscheduler.readthedocs.io

Asynchronously
^^^^^^^^^^^^^^

.. code-block:: python

    from apscheduler.schedulers.asyncio import AsyncIOScheduler

    from pyrogram import Client

    app = Client("my_account")


    async def job():
        await app.send_message("me", "Hi!")


    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, "interval", seconds=3)

    scheduler.start()
    app.run()

Non-Asynchronously
^^^^^^^^^^^^^^^^^^

.. code-block:: python

    from apscheduler.schedulers.background import BackgroundScheduler

    from pyrogram import Client

    app = Client("my_account")


    def job():
        app.send_message("me", "Hi!")


    scheduler = BackgroundScheduler()
    scheduler.add_job(job, "interval", seconds=3)

    scheduler.start()
    app.run()

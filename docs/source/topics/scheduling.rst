Scheduling Tasks
================

Scheduling tasks means executing one or more functions periodically at pre-defined intervals or after a delay. This is
useful, for example, to send recurring messages to specific chats or users.

Since there's no built-in task scheduler in Pyrogram, this page will only show examples on how to integrate Pyrogram
with the main Python schedule libraries such as ``schedule`` and ``apscheduler``. For more detailed information, you can
visit and learn from each library documentation.

Using ``schedule``
------------------

- Install with ``pip3 install schedule``
- Documentation: https://schedule.readthedocs.io

.. code-block:: python

    import time

    import schedule

    from pyrogram import Client

    app = Client("my_account")


    def job():
        app.send_message("me", "Hi!")


    schedule.every(3).seconds.do(job)

    with app:
        while True:
            schedule.run_pending()
            time.sleep(1)



Using ``apscheduler``
---------------------

- Install with ``pip3 install apscheduler``
- Documentation: https://apscheduler.readthedocs.io

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

``apscheduler`` does also support async code, here's an example with
`Pyrogram Asyncio <https://docs.pyrogram.org/intro/install.html#asynchronous>`_:

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


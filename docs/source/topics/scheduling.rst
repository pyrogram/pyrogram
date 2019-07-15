Scheduling tasks
================

Pyrogram itself as Telegram MTProto API Framework contains only stuff
related to Telegram. Scheduling is out of it's scope.

But it is easy to integrate pyrogram with your favourite scheduler.

schedule
--------

Note that schedule is not suitable for async version of pyrogram.

.. code-block:: python

    import time
    import schedule


    def job():
        app.send_message("me", "Hi!")


    schedule.every(10).minutes.do(job)
    schedule.every().hour.do(job)
    schedule.every().day.at("10:30").do(job)
    schedule.every(5).to(10).minutes.do(job)
    schedule.every().monday.do(job)
    schedule.every().wednesday.at("13:15").do(job)
    schedule.every().minute.at(":17").do(job)

    with app:
        while True:
            schedule.run_pending()
            time.sleep(1)


apscheduler
-----------

.. code-block:: python

    import time
    from apscheduler.schedulers.background import BackgroundScheduler


    def job():
        app.send_message("me", "Hi!")


    scheduler = BackgroundScheduler()
    scheduler.add_job(job, 'interval', seconds=3)

    scheduler.start()
    app.run()

Apscheduler supports async version of pyrogram too, here is async example:

.. code-block:: python

    from apscheduler.schedulers.asyncio import AsyncIOScheduler


    async def job():
        await app.send_message("me", "Hi!")


    scheduler = AsyncIOScheduler()
    scheduler.add_job(job, 'interval', seconds=3)

    scheduler.start()
    app.run()


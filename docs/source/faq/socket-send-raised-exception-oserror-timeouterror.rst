socket.send() raised exception, OSError(), TimeoutError()
=========================================================

If you get this error chances are you or Telegram ended up with a slow or inconsistent network connection, which
triggers internal timeouts due to data not being sent/received in time. Another reason could be because you are blocking
the event loop for too long, most likely due to an improper use of non-asynchronous or threaded operations which may
lead to blocking code that prevents the event loop from running properly.

You can consider the following:

- Use Pyrogram asynchronously in its intended way.
- Use shorter non-asynchronous processing loops.
- Use ``asyncio.sleep()`` instead of ``time.sleep()``.

socket.send(), OSError(), TimeoutError(), Connection lost/reset
===============================================================

If you get any of these errors chances are you ended up with a slow or inconsistent network connection.
Another reason could be because you are blocking the event loop for too long.

You can consider the following:

- Use Pyrogram asynchronously in its intended way.
- Use shorter non-asynchronous processing loops.
- Use ``asyncio.sleep()`` instead of ``time.sleep()``.
- Use a stable network connection.

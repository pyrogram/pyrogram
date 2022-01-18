socket.send() raised exception, OSError(), TimeoutError()
=========================================================

If you get this error chances are you are blocking the event loop for too long.
In general, it means you are executing thread-blocking code that prevents the event loop from
running properly. For example:

- You are using ``time.sleep()`` instead of ``asyncio.sleep()``.
- You are running processing loops that take too much time to complete.
- You are reading/writing files to disk that take too much time to complete.
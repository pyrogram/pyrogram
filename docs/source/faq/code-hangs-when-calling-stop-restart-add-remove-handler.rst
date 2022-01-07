Code hangs when calling stop, restart, add/remove_handler
=========================================================

You tried to ``.stop()``, ``.restart()``, ``.add_handler()`` or ``.remove_handler()`` inside a running handler, but
that can't be done because the way Pyrogram deals with handlers would make it hang.

When calling one of the methods above inside an event handler, Pyrogram needs to wait for all running handlers to finish
in order to continue. Since your handler is blocking the execution by waiting for the called method to finish
and since Pyrogram needs to wait for your handler to finish, you are left with a deadlock.

The solution to this problem is to pass ``block=False`` to such methods so that they return immediately and the actual
code called asynchronously.
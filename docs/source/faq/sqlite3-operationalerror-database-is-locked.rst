sqlite3.OperationalError: database is locked
============================================

This error occurs when more than one process is using the same session file, that is, when you run two or more clients
at the same time using the same session name or in case another program has accessed the file.

For example, it could occur when a background script is still running and you forgot about it. In this case, you either
restart your system or find and kill the process that is locking the database. On Unix based systems, you can try the
following:

#. ``cd`` into your session file directory.
#. ``fuser my_account.session`` to find the process id.
#. ``kill 1234`` to gracefully stop the process.
#. If the last command doesn't help, use ``kill -9 1234`` instead.

If you want to run multiple clients on the same account, you must authorize your account (either user or bot)
from the beginning every time, and use different session names for each parallel client you are going to use.
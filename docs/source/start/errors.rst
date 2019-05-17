Error Handling
==============

Errors are inevitable when working with the API, and they must be correctly handled with ``try..except`` blocks in order
to control the behaviour of your application. Pyrogram errors all live inside the ``errors`` package:

.. code-block:: python

    from pyrogram import errors

RPCError
--------

The father of all errors is named ``RPCError``. This error exists in form of a Python exception which is directly
subclass-ed from Python's main ``Exception`` and is able to catch all Telegram API related errors. This error is raised
every time a method call against Telegram's API was unsuccessful.

.. code-block:: python

    from pyrogram.errors import RPCError

.. warning::

    It must be noted that catching this error is bad practice, especially when no feedback is given (i.e. by
    logging/printing the full error traceback), because it makes it impossible to understand what went wrong.

Error Categories
----------------

The ``RPCError`` packs together all the possible errors Telegram could raise, but to make things tidier, Pyrogram
provides categories of errors, which are named after the common HTTP errors and subclass-ed from the RPCError:

.. code-block:: python

    from pyrogram.errors import BadRequest, Forbidden, ...

-   `303 - SeeOther <../api/errors#seeother>`_
-   `400 - BadRequest <../api/errors#badrequest>`_
-   `401 - Unauthorized  <../api/errors#unauthorized>`_
-   `403 - Forbidden <../api/errors#forbidden>`_
-   `406 - NotAcceptable <../api/errors#notacceptable>`_
-   `420 - Flood <../api/errors#flood>`_
-   `500 - InternalServerError <../api/errors#internalservererror>`_

Single Errors
-------------

For a fine-grained control over every single error, Pyrogram does also expose errors that deal each with a specific
issue. For example:

.. code-block:: python

    from pyrogram.errors import FloodWait

These errors subclass directly from the category of errors they belong to, which in turn subclass from the father
RPCError, thus building a class of error hierarchy such as this:

- RPCError
    - BadRequest
        - ``MessageEmpty``
        - ``UsernameOccupied``
        - ``...``
    - InternalServerError
        - ``RpcCallFail``
        - ``InterDcCallError``
        - ``...``
    - ``...``

.. _Errors: api/errors

Unknown Errors
--------------

In case Pyrogram does not know anything yet about a specific error, it raises a special ``520 - UnknownError`` exception
and logs it in the ``unknown_errors.txt`` file. Users are invited to report these unknown errors.

Errors with Values
------------------

Exception objects may also contain some informative values. For example, ``FloodWait`` holds the amount of seconds you
have to wait before you can try again. The value is always stored in the ``x`` field of the returned exception object:

.. code-block:: python

    import time
    from pyrogram.errors import FloodWait

    try:
        ...
    except FloodWait as e:
        time.sleep(e.x)  # Wait before trying again

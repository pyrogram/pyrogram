Error Handling
==============

Errors are inevitable when working with the API, and they must be correctly handled with ``try..except`` blocks.

There are many errors that Telegram could return, but they all fall in one of these categories
(which are in turn children of the ``RPCError`` superclass):

-   `303 - See Other <../api/errors#see-other>`_
-   `400 - Bad Request <../api/errors#bad-request>`_
-   `401 - Unauthorized  <../api/errors#unauthorized>`_
-   `403 - Forbidden <../api/errors#forbidden>`_
-   `406 - Not Acceptable <../api/errors#not-acceptable>`_
-   `420 - Flood <../api/errors#flood>`_
-   `500 - Internal Server Error <../api/errors#internal-server-error>`_

As stated above, there are really many (too many) errors, and in case Pyrogram does not know anything yet about a
specific one, it raises a special ``520 Unknown Error`` exception and logs it
in the ``unknown_errors.txt`` file. Users are invited to report these unknown errors.

Examples
--------

.. code-block:: python

    from pyrogram.errors import (
        BadRequest, Flood, InternalServerError,
        SeeOther, Unauthorized, UnknownError
    )

    try:
        ...
    except BadRequest:
        pass
    except Flood:
        pass
    except InternalServerError:
        pass
    except SeeOther:
        pass
    except Unauthorized:
        pass
    except UnknownError:
        pass

Exception objects may also contain some informative values.
E.g.: ``FloodWait`` holds the amount of seconds you have to wait
before you can try again. The value is always stored in the ``x`` field of the returned exception object:

.. code-block:: python

    import time
    from pyrogram.errors import FloodWait

    try:
        ...
    except FloodWait as e:
        time.sleep(e.x)

Error Handling
==============

Errors are inevitable when working with the API, and they must be correctly handled by
the use of ``try..except`` blocks.

There are many errors that Telegram could return, but they all fall in one of these five exception categories
(which are in turn children of the :obj:`pyrogram.Error` superclass)

-   :obj:`303 See Other <pyrogram.api.errors.SeeOther>`
-   :obj:`400 Bad Request <pyrogram.api.errors.BadRequest>`
-   :obj:`401 Unauthorized <pyrogram.api.errors.Unauthorized>`
-   :obj:`420 Flood <pyrogram.api.errors.Flood>`
-   :obj:`500 Internal Server Error <pyrogram.api.errors.InternalServerError>`

As stated above, there are really many (too many) errors, and in case Pyrogram does not know anything yet about a
specific one, it raises a special :obj:`520 Unknown Error <pyrogram.api.errors.UnknownError>` exception and logs it
in the ``unknown_errors.txt`` file. Users are invited to report these unknown errors; in later versions of Pyrogram
some kind of automatic error reporting module might be implemented.

Examples
--------

.. code-block:: python

    from pyrogram.api.errors import (
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
E.g.: :obj:`FloodWait <pyrogram.api.errors.exceptions.flood_420.FloodWait>` holds the amount of seconds you have to wait
before you can try again. The value is always stored in the ``x`` field of the returned exception object:

.. code-block:: python

    import time
    from pyrogram.api.errors import FloodWait

    try:
        ...
    except FloodWait as e:
        time.sleep(e.x)

**TODO: Better explanation on how to deal with exceptions**
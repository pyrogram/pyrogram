Error Handling
==============

Errors are inevitable when working with the API, and they must be correctly handled with ``try..except`` blocks.

There are many errors that Telegram could return, but they all fall in one of these categories
(which are in turn children of the :obj:`RPCError <pyrogram.RPCError>` superclass):

-   :obj:`303 - See Other <pyrogram.errors.SeeOther>`
-   :obj:`400 - Bad Request <pyrogram.errors.BadRequest>`
-   :obj:`401 - Unauthorized <pyrogram.errors.Unauthorized>`
-   :obj:`403 - Forbidden <pyrogram.errors.Forbidden>`
-   :obj:`406 - Not Acceptable <pyrogram.errors.NotAcceptable>`
-   :obj:`420 - Flood <pyrogram.errors.Flood>`
-   :obj:`500 - Internal Server Error <pyrogram.errors.InternalServerError>`

As stated above, there are really many (too many) errors, and in case Pyrogram does not know anything yet about a
specific one, it raises a special :obj:`520 Unknown Error <pyrogram.errors.UnknownError>` exception and logs it
in the ``unknown_errors.txt`` file. Users are invited to report these unknown errors; in later versions of Pyrogram
some kind of automatic error reporting module might be implemented.

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
E.g.: :obj:`FloodWait <pyrogram.errors.exceptions.flood_420.FloodWait>` holds the amount of seconds you have to wait
before you can try again. The value is always stored in the ``x`` field of the returned exception object:

.. code-block:: python

    import time
    from pyrogram.errors import FloodWait

    try:
        ...
    except FloodWait as e:
        time.sleep(e.x)

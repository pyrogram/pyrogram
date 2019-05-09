Errors
======

All the Pyrogram errors listed here live inside the ``errors`` sub-package.

**Example:**

.. code-block:: python

    from pyrogram.errors import RPCError

    try:
        ...
    except RPCError:
        ...

.. autoexception:: pyrogram.RPCError()
    :members:

.. toctree::
    ../errors/SeeOther
    ../errors/BadRequest
    ../errors/Unauthorized
    ../errors/Forbidden
    ../errors/NotAcceptable
    ../errors/Flood
    ../errors/InternalServerError
    ../errors/UnknownError

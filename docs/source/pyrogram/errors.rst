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
    ../errors/see-other
    ../errors/bad-request
    ../errors/unauthorized
    ../errors/forbidden
    ../errors/not-acceptable
    ../errors/flood
    ../errors/internal-server-error
    ../errors/unknown-error

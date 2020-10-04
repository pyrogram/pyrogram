RPC Errors
==========

All Pyrogram API errors live inside the ``errors`` sub-package: ``pyrogram.errors``.
The errors ids listed here are shown as *UPPER_SNAKE_CASE*, but the actual exception names to import from Pyrogram
follow the usual *PascalCase* convention.

.. code-block:: python

    from pyrogram.errors import FloodWait

    try:
        ...
    except FloodWait as e:
        ...

.. hlist::
    :columns: 1

    - :doc:`see-other`
    - :doc:`bad-request`
    - :doc:`unauthorized`
    - :doc:`forbidden`
    - :doc:`not-acceptable`
    - :doc:`flood`
    - :doc:`internal-server-error`

.. toctree::
    :hidden:

    see-other
    bad-request
    unauthorized
    forbidden
    not-acceptable
    flood
    internal-server-error
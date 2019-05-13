RPC Errors
==========

All Pyrogram API errors live inside the ``errors`` sub-package: ``pyrogram.errors``.
The errors ids listed here are shown as *UPPER_SNAKE_CASE*, but the actual exception names to import from Pyrogram
follow the usual *PascalCase* convention.

**Example**:

.. code-block:: python

    from pyrogram.errors import InternalServerError

    try:
        ...
    except FloodWait:
        ...

303 - See Other
---------------

.. csv-table::
    :file: ../../../compiler/error/source/303_SEE_OTHER.tsv
    :delim: tab
    :header-rows: 1

400 - Bad Request
-----------------

.. csv-table::
    :file: ../../../compiler/error/source/400_BAD_REQUEST.tsv
    :delim: tab
    :header-rows: 1

401 - Unauthorized
------------------

.. csv-table::
    :file: ../../../compiler/error/source/401_UNAUTHORIZED.tsv
    :delim: tab
    :header-rows: 1

403 - Forbidden
---------------

.. csv-table::
    :file: ../../../compiler/error/source/403_FORBIDDEN.tsv
    :delim: tab
    :header-rows: 1

406 - Not Acceptable
--------------------

.. csv-table::
    :file: ../../../compiler/error/source/406_NOT_ACCEPTABLE.tsv
    :delim: tab
    :header-rows: 1

420 - Flood
-----------

.. csv-table::
    :file: ../../../compiler/error/source/420_FLOOD.tsv
    :delim: tab
    :header-rows: 1

500 - Internal Server Error
---------------------------

.. csv-table::
    :file: ../../../compiler/error/source/500_INTERNAL_SERVER_ERROR.tsv
    :delim: tab
    :header-rows: 1

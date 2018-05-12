Quick Installation
==================

-   The easiest way to install and upgrade Pyrogram is by using **pip**:

    .. code-block:: bash

        $ pip3 install --upgrade pyrogram

-   or, with TgCrypto_ (recommended):

    .. code-block:: bash

        $ pip3 install --upgrade pyrogram[tgcrypto]

Bleeding Edge
-------------

If you want the latest development version of the library, you can install it with:

.. code-block:: bash

    $ pip3 install --upgrade git+https://github.com/pyrogram/pyrogram.git

Verifying
---------

To verify that Pyrogram is correctly installed, open a Python shell and import it.
If no error shows up you are good to go.

.. code-block:: bash

    >>> import pyrogram
    >>> pyrogram.__version__
    '0.7.4'

.. _TgCrypto: https://docs.pyrogram.ml/resources/TgCrypto
Installation
============

Being a Python library, Pyrogram requires Python to be installed in your system.
We recommend using the latest version of Python 3 and pip.

Get Python 3 from https://www.python.org/downloads/ or with your package manager and pip
by following the instructions at https://pip.pypa.io/en/latest/installing/.

.. note::
    Pyrogram supports Python 3 only, starting from version 3.4 and PyPy.

Install Pyrogram
----------------

-   The easiest way to install and upgrade Pyrogram is by using **pip**:

    .. code-block:: bash

        $ pip3 install --upgrade pyrogram

-   or, with TgCrypto_ (recommended):

    .. code-block:: bash

        $ pip3 install --upgrade pyrogram[tgcrypto]

Bleeding Edge
-------------

If you want the latest development version of Pyrogram, you can install it straight from the develop_
branch using this command:

.. code-block:: bash

    $ pip3 install --upgrade git+https://github.com/pyrogram/pyrogram.git

Verifying
---------

To verify that Pyrogram is correctly installed, open a Python shell and import it.
If no error shows up you are good to go.

.. code-block:: bash

    >>> import pyrogram
    >>> pyrogram.__version__
    '0.8.0'

.. _TgCrypto: https://docs.pyrogram.ml/resources/TgCrypto
.. _develop: http://github.com/pyrogram/pyrogram
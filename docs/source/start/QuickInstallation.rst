Quick Installation
==================

The most straightforward and recommended way to install or upgrade Pyrogram is by using **pip**:

.. code-block:: bash

    $ pip install --upgrade pyrogram

Or, with TgCrypto_:

.. code-block:: bash

    $ pip install --upgrade pyrogram[tgcrypto]

.. important::

    Pyrogram only works on Python 3.3 or higher; if your **pip** points to Python 2.x use **pip3** instead.

Bleeding Edge
-------------

If you want the latest development version of the library, you can either install it automatically with:

.. code-block:: bash

    $ pip install --upgrade git+https://github.com/pyrogram/pyrogram.git

or manually, using:

.. code-block:: bash

    $ git clone https://github.com/pyrogram/pyrogram.git
    $ cd pyrogram
    $ python setup.py install

Verifying
---------

To verify that Pyrogram is correctly installed, open a Python shell and try to import it.
If no errors show up you are good to go.

.. code-block:: bash

    >>> import pyrogram
    >>> pyrogram.__version__
    '0.6.1'

.. _TgCrypto: https://docs.pyrogram.ml/resources/TgCrypto
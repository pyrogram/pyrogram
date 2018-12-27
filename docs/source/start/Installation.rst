Installation
============

Being a Python library, Pyrogram requires Python to be installed in your system.
We recommend using the latest version of Python 3 and pip.

Get Python 3 from https://www.python.org/downloads/ (or with your package manager) and pip
by following the instructions at https://pip.pypa.io/en/latest/installing/.

.. important::

    Pyrogram supports **Python 3** only, starting from version 3.4. **PyPy** is supported too.

Install Pyrogram
----------------

-   The easiest way to install and upgrade Pyrogram to its latest stable version is by using **pip**:

    .. code-block:: text

        $ pip3 install --upgrade pyrogram

-   or, with TgCrypto_ as extra requirement (recommended):

    .. code-block:: text

        $ pip3 install --upgrade pyrogram[fast]

Bleeding Edge
-------------

If you want the latest development version of Pyrogram, you can install it straight from the develop_
branch using this command (you might need to install **git** first):

.. code-block:: text

    $ pip3 install --upgrade git+https://github.com/pyrogram/pyrogram.git

Asynchronous
------------

Pyrogram heavily depends on IO-bound network code (it's a cloud-based messaging client library after all), and here's
where asyncio shines the most by providing extra performance while running on a single OS-level thread only.

**A fully asynchronous variant of Pyrogram is therefore available** (Python 3.5+ required).
Use this command to install:

.. code-block:: text

    $ pip3 install --upgrade git+https://github.com/pyrogram/pyrogram.git@asyncio


Pyrogram API remains the same and features are kept up to date from the non-async, default develop branch, but you
are obviously required Python asyncio knowledge in order to take full advantage of it.


.. tip::

    The idea to turn Pyrogram fully asynchronous is still under consideration, but is wise to expect that in future this
    would be the one and only way to work with Pyrogram.

    You can start using Pyrogram Async variant right now as an excuse to learn more about asynchronous programming and
    do experiments with it!

.. raw:: html

    <script async
        src="https://telegram.org/js/telegram-widget.js?4"
        data-telegram-post="Pyrogram/4"
        data-width="100%">
    </script>

.. centered:: Subscribe to `@Pyrogram <https://t.me/Pyrogram>`_ for news and announcements

Verifying
---------

To verify that Pyrogram is correctly installed, open a Python shell and import it.
If no error shows up you are good to go.

.. code-block:: python

    >>> import pyrogram
    >>> pyrogram.__version__
    '0.9.4'

.. _TgCrypto: https://docs.pyrogram.ml/resources/TgCrypto
.. _develop: http://github.com/pyrogram/pyrogram

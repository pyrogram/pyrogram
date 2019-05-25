Install Guide
=============

Being a Python library, **Pyrogram** requires Python to be installed in your system.
We recommend using the latest versions of both Python 3 and pip.

- Get **Python 3** from https://www.python.org/downloads/ (or with your package manager)
- Get **pip** by following the instructions at https://pip.pypa.io/en/latest/installing/.

.. important::

    Pyrogram supports **Python 3** only, starting from version 3.4. **PyPy** is supported too.

Install Pyrogram
----------------

-   The easiest way to install and upgrade Pyrogram to its latest stable version is by using **pip**:

    .. code-block:: text

        $ pip3 install -U pyrogram

-   or, with TgCrypto_ as extra requirement (recommended):

    .. code-block:: text

        $ pip3 install -U pyrogram[fast]

Bleeding Edge
-------------

Pyrogram is always evolving, although new releases on PyPI are published only when enough changes are added, but this
doesn't mean you can't try new features right now!

In case you'd like to try out the latest Pyrogram features, the `GitHub repo`_ is always kept updated with new changes;
you can install the development version straight from the ``develop`` branch using this command (note "develop.zip" in
the link):

.. code-block:: text

    $ pip3 install -U https://github.com/pyrogram/pyrogram/archive/develop.zip

Asynchronous
------------

Pyrogram heavily depends on IO-bound network code (it's a cloud-based messaging framework after all), and here's
where asyncio shines the most by providing extra performance and efficiency while running on a single OS-level thread
only.

**A fully asynchronous variant of Pyrogram is therefore available** (Python 3.5.3+ required).
Use this command to install (note "asyncio.zip" in the link):

.. code-block:: text

    $ pip3 install -U https://github.com/pyrogram/pyrogram/archive/asyncio.zip


Pyrogram's API remains the same and features are kept up to date from the non-async, default develop branch, but you
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

.. parsed-literal::

    >>> import pyrogram
    >>> pyrogram.__version__
    '|version|'

.. _TgCrypto: ../topics/tgcrypto
.. _`Github repo`: http://github.com/pyrogram/pyrogram

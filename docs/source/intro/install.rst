Install Guide
=============

Being a modern Python framework, Pyrogram requires an up to date version of Python to be installed in your system.
We recommend using the latest versions of both Python 3 and pip.

.. contents:: Contents
    :backlinks: none
    :depth: 1
    :local:

-----

Install Pyrogram
----------------

-   The easiest way to install and upgrade Pyrogram to its latest stable version is by using **pip**:

    .. code-block:: text

        $ pip3 install -U pyrogram

-   or, with :doc:`TgCrypto <../topics/tgcrypto>` as extra requirement (recommended):

    .. code-block:: text

        $ pip3 install -U pyrogram tgcrypto

Bleeding Edge
-------------

You can install the development version from the git ``master`` branch using this command:

.. code-block:: text

    $ pip3 install -U https://github.com/pyrogram/pyrogram/archive/master.zip

Verifying
---------

To verify that Pyrogram is correctly installed, open a Python shell and import it.
If no error shows up you are good to go.

.. parsed-literal::

    >>> import pyrogram
    >>> pyrogram.__version__
    'x.y.z'

.. _`Github repo`: http://github.com/pyrogram/pyrogram

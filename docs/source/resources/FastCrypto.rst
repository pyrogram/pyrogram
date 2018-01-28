Fast Crypto
===========

Pyrogram's speed can be *dramatically* boosted up by installing TgCrypto_, a high-performance, easy-to-install crypto
library specifically written in C for Pyrogram [#f1]_. TgCrypto is a replacement for the painfully slow PyAES and
implements the required crypto algorithms MTProto requires, namely AES-IGE and AES-CTR 256 bit.

Installation
------------

.. code-block:: bash

    $ pip install --upgrade tgcrypto


.. note:: Being a C extension for Python, TgCrypto is an optional but *highly recommended* dependency; when TgCrypto
   is not detected on your system, Pyrogram will automatically fall back to PyAES and will show you a warning.

The reason about being an optional package is that TgCrypto requires some extra system tools in order to be compiled.
Usually the errors you receive when trying to install TgCrypto are enough to understand what you should do next.

-  **Windows**: Install `Visual C++ 2015 Build Tools <http://landinghub.visualstudio.com/visual-cpp-build-tools>`_.

-  **macOS**: A pop-up will automatically ask you to install the command line developer tools as soon as you issue the
   installation command.

-  **Linux**: Depending on your distro, install a proper C compiler (``gcc``, ``clang``) and the Python header files
   (``python3-dev``).

-  **Termux (Android)**: Install ``clang`` and ``python-dev`` packages.

More help on the `Pyrogram group chat <https://t.me/PyrogramChat>`_.

.. _TgCrypto: https://github.com/pyrogram/tgcrypto

.. [#f1] Although TgCrypto is intended for Pyrogram, it is shipped as a standalone package and can thus be used for
   other projects too.
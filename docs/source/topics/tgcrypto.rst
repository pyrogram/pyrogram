Fast Crypto
===========

Pyrogram's speed can be *dramatically* boosted up by TgCrypto_, a high-performance, easy-to-install Telegram Crypto
Library specifically written in C for Pyrogram [1]_ as a Python extension.

TgCrypto is a replacement for the much slower PyAES and implements the crypto algorithms Telegram requires, namely
**AES-IGE 256 bit** (used in MTProto v2.0) and **AES-CTR 256 bit** (used for CDN encrypted files).

Installation
------------

.. code-block:: bash

    $ pip3 install -U tgcrypto

.. note:: Being a C extension for Python, TgCrypto is an optional but *highly recommended* dependency; when TgCrypto is
   not detected in your system, Pyrogram will automatically fall back to PyAES and will show you a warning.

The reason about being an optional package is that TgCrypto requires some extra system tools in order to be compiled.
The errors you receive when trying to install TgCrypto are system dependent, but also descriptive enough to understand
what you should do next:

-  **Windows**: Install `Visual C++ 2015 Build Tools <https://www.microsoft.com/en-us/download/details.aspx?id=48159>`_.
-  **macOS**: A pop-up will automatically ask you to install the command line developer tools.
-  **Linux**: Install a proper C compiler (``gcc``, ``clang``) and the Python header files (``python3-dev``).
-  **Termux (Android)**: Install ``clang`` package.

.. _TgCrypto: https://github.com/pyrogram/tgcrypto

.. [1] Although TgCrypto is intended for Pyrogram, it is shipped as a standalone package and can thus be used for
   other Python projects too.

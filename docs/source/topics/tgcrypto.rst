Fast Crypto
===========

Pyrogram's speed can be boosted up by TgCrypto_, a high-performance, easy-to-install cryptography library specifically
written in C for Pyrogram as a Python extension.

TgCrypto is a replacement for a slower Python-only alternative and implements the cryptographic algorithms Telegram
requires, namely: AES-256-IGE, AES-256-CTR and AES-256-CBC.

Installation
------------

.. code-block:: bash

    $ pip3 install -U tgcrypto

.. note:: When TgCrypto is not detected in your system, Pyrogram will automatically fall back to a slower Python-only
    implementation and will show you a warning.

The reason about being an optional package is that TgCrypto requires extra system tools in order to be compiled.
The errors you receive when trying to install TgCrypto are system dependent, but also descriptive enough to understand
what you should do next:

- **Windows**: Install `Visual C++ 2015 Build Tools <https://www.microsoft.com/en-us/download/details.aspx?id=48159>`_.
- **macOS**: A pop-up will automatically ask you to install the command line developer tools.
- **Linux**: Install a proper C compiler (``gcc``, ``clang``) and the Python header files (``python3-dev``).
- **Termux**: Install ``clang`` package.

.. _TgCrypto: https://github.com/pyrogram/tgcrypto
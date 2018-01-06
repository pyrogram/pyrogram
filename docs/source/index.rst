Welcome to Pyrogram
===================

.. raw:: html

    <div align="center">
        <a href="https://pyrogram.ml">
            <img src="https://pyrogram.ml/images/logo2.png" alt="Logo">
        </a>
    </div>

    <p align="center">
        <b>Telegram MTProto API Client Library for Python</b>
    </p>

Preview
-------

.. code-block:: python

    from pyrogram import Client

    client = Client("example")
    client.start()

    client.send_message("me", "Hi there! I'm using Pyrogram")
    client.send_photo("me", "/home/dan/pic.jpg", "Nice photo!")

    client.stop()

About
-----

Welcome to the Pyrogram's documentation! Here you can find resources for learning how to use the library.
Contents are organized by topic and are accessible from the sidebar.

To get started, press Next.

.. toctree::
    :hidden:
    :caption: Getting Started

    getting_started/QuickInstallation
    getting_started/ProjectSetup
    getting_started/BasicUsage

.. toctree::
    :hidden:
    :caption: Resources

    resources/TextFormatting
    resources/UpdateHandling
    resources/ErrorHandling

.. toctree::
    :hidden:
    :caption: Main Package

    pyrogram/index

.. toctree::
    :hidden:
    :caption: Telegram API

    functions/index
    types/index

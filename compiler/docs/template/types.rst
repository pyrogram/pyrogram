Available Types
===============

This page is about Pyrogram Types. All types listed here are available through the ``pyrogram.types`` package.
Unless required as argument to a client method, most of the types don't need to be manually instantiated because they
are only returned by other methods. You also don't need to import them, unless you want to type-hint your variables.

.. code-block:: python

    from pyrogram.types import User, Message, ...

.. note::

    Optional fields always exist inside the object, but they could be empty and contain the value of ``None``.
    Empty fields aren't shown when, for example, using ``print(message)`` and this means that
    ``hasattr(message, "photo")`` always returns ``True``.

    To tell whether a field is set or not, do a simple boolean check: ``if message.photo: ...``.

.. contents:: Contents
    :backlinks: none
    :local:

-----

.. currentmodule:: pyrogram.types

Users & Chats
-------------

.. autosummary::
    :nosignatures:

    {users_chats}

.. toctree::
    :hidden:

    {users_chats}

Messages & Media
----------------

.. autosummary::
    :nosignatures:

    {messages_media}

.. toctree::
    :hidden:

    {messages_media}

Bots & Keyboards
----------------

.. autosummary::
    :nosignatures:

    {bots_keyboard}

.. toctree::
    :hidden:

    {bots_keyboard}

Input Media
-----------

.. autosummary::
    :nosignatures:

    {input_media}

.. toctree::
    :hidden:

    {input_media}

Inline Mode
-----------

.. autosummary::
    :nosignatures:

    {inline_mode}

.. toctree::
    :hidden:

    {inline_mode}

InputMessageContent
-------------------

.. autosummary::
    :nosignatures:

    {input_message_content}

.. toctree::
    :hidden:

    {input_message_content}

Authorization
-------------

.. autosummary::
    :nosignatures:

    {authorization}

.. toctree::
    :hidden:

    {authorization}
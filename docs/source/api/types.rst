Available Types
===============

This page is about Pyrogram types. All types listed here are accessible through the main package directly.

.. code-block:: python
    :emphasize-lines: 1

    from pyrogram import User, Message, ...

.. note::

    **Optional** fields may not exist when irrelevant -- i.e.: they will contain the value of ``None`` and aren't shown
    when, for example, using ``print()``.

.. currentmodule:: pyrogram

Index
-----

Users & Chats
^^^^^^^^^^^^^

.. hlist::
    :columns: 5

    - :class:`User`
    - :class:`UserStatus`
    - :class:`Chat`
    - :class:`ChatPreview`
    - :class:`ChatPhoto`
    - :class:`ChatMember`
    - :class:`ChatPermissions`
    - :class:`Dialog`

Messages & Media
^^^^^^^^^^^^^^^^

.. hlist::
    :columns: 5

    - :class:`Message`
    - :class:`MessageEntity`
    - :class:`Photo`
    - :class:`Thumbnail`
    - :class:`Audio`
    - :class:`Document`
    - :class:`Animation`
    - :class:`Video`
    - :class:`Voice`
    - :class:`VideoNote`
    - :class:`Contact`
    - :class:`Location`
    - :class:`Venue`
    - :class:`Sticker`
    - :class:`Game`
    - :class:`Poll`
    - :class:`PollOption`

Bots & Keyboards
^^^^^^^^^^^^^^^^

.. hlist::
    :columns: 4

    - :class:`ReplyKeyboardMarkup`
    - :class:`KeyboardButton`
    - :class:`ReplyKeyboardRemove`
    - :class:`InlineKeyboardMarkup`
    - :class:`InlineKeyboardButton`
    - :class:`ForceReply`
    - :class:`CallbackQuery`
    - :class:`GameHighScore`
    - :class:`CallbackGame`

Input Media
^^^^^^^^^^^

.. hlist::
    :columns: 4

    - :class:`InputMedia`
    - :class:`InputMediaPhoto`
    - :class:`InputMediaVideo`
    - :class:`InputMediaAudio`
    - :class:`InputMediaAnimation`
    - :class:`InputMediaDocument`
    - :class:`InputPhoneContact`

Inline Mode
^^^^^^^^^^^

.. hlist::
    :columns: 3

    - :class:`InlineQuery`
    - :class:`InlineQueryResult`
    - :class:`InlineQueryResultArticle`

InputMessageContent
^^^^^^^^^^^^^^^^^^^

.. hlist::
    :columns: 3

    - :class:`InputMessageContent`
    - :class:`InputTextMessageContent`

-----

Details
-------

..  User & Chats
.. autoclass:: User()
.. autoclass:: UserStatus()
.. autoclass:: Chat()
.. autoclass:: ChatPreview()
.. autoclass:: ChatPhoto()
.. autoclass:: ChatMember()
.. autoclass:: ChatPermissions()
.. autoclass:: Dialog()

..  Messages & Media
.. autoclass:: Message()
.. autoclass:: MessageEntity()
.. autoclass:: Photo()
.. autoclass:: Thumbnail()
.. autoclass:: Audio()
.. autoclass:: Document()
.. autoclass:: Animation()
.. autoclass:: Video()
.. autoclass:: Voice()
.. autoclass:: VideoNote()
.. autoclass:: Contact()
.. autoclass:: Location()
.. autoclass:: Venue()
.. autoclass:: Sticker()
.. autoclass:: Game()
.. autoclass:: Poll()
.. autoclass:: PollOption()

..  Bots & Keyboards
.. autoclass:: ReplyKeyboardMarkup()
.. autoclass:: KeyboardButton()
.. autoclass:: ReplyKeyboardRemove()
.. autoclass:: InlineKeyboardMarkup()
.. autoclass:: InlineKeyboardButton()
.. autoclass:: ForceReply()
.. autoclass:: CallbackQuery()
.. autoclass:: GameHighScore()
.. autoclass:: CallbackGame()

..  Input Media
.. autoclass:: InputMedia()
.. autoclass:: InputMediaPhoto()
.. autoclass:: InputMediaVideo()
.. autoclass:: InputMediaAudio()
.. autoclass:: InputMediaAnimation()
.. autoclass:: InputMediaDocument()
.. autoclass:: InputPhoneContact()

..  Inline Mode
.. autoclass:: InlineQuery()
.. autoclass:: InlineQueryResult()
.. autoclass:: InlineQueryResultArticle()

..  InputMessageContent
.. autoclass:: InputMessageContent()
.. autoclass:: InputTextMessageContent()

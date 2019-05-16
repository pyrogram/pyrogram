Available Types
===============

All Pyrogram types listed here are accessible through the main package directly.

.. code-block:: python
    :emphasize-lines: 1

    from pyrogram import User, Message, ...

.. note::

    **Optional** fields may not exist when irrelevant -- i.e.: they will contain the value of ``None`` and aren't shown
    when, for example, using ``print()``.

.. currentmodule:: pyrogram

Users & Chats
-------------

.. autosummary::
    :nosignatures:

    User
    UserStatus
    Chat
    ChatPreview
    ChatPhoto
    ChatMember
    ChatMembers
    ChatPermissions
    Dialog
    Dialogs

Messages & Media
----------------

.. autosummary::
    :nosignatures:

    Message
    Messages
    MessageEntity
    Photo
    PhotoSize
    UserProfilePhotos
    Audio
    Document
    Animation
    Video
    Voice
    VideoNote
    Contact
    Location
    Venue
    Sticker
    Game
    Poll
    PollOption

Keyboards
---------

.. autosummary::
    :nosignatures:

    ReplyKeyboardMarkup
    KeyboardButton
    ReplyKeyboardRemove
    InlineKeyboardMarkup
    InlineKeyboardButton
    ForceReply
    CallbackQuery
    GameHighScore
    CallbackGame

Input Media
-----------

.. autosummary::
    :nosignatures:

    InputMedia
    InputMediaPhoto
    InputMediaVideo
    InputMediaAudio
    InputMediaAnimation
    InputMediaDocument
    InputPhoneContact

Inline Mode
------------

.. autosummary::
    :nosignatures:

    InlineQuery
    InlineQueryResult
    InlineQueryResultArticle

InputMessageContent
-------------------

.. autosummary::
    :nosignatures:

    InputMessageContent
    InputTextMessageContent

..  User & Chats
    ------------

.. autoclass:: User()
.. autoclass:: UserStatus()
.. autoclass:: Chat()
.. autoclass:: ChatPreview()
.. autoclass:: ChatPhoto()
.. autoclass:: ChatMember()
.. autoclass:: ChatMembers()
.. autoclass:: ChatPermissions()
.. autoclass:: Dialog()
.. autoclass:: Dialogs()

..  Messages & Media
    ----------------

.. autoclass:: Message()
.. autoclass:: Messages()
.. autoclass:: MessageEntity()
.. autoclass:: Photo()
.. autoclass:: PhotoSize()
.. autoclass:: UserProfilePhotos()
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

..  Keyboards
    ---------

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
    -----------

.. autoclass:: InputMedia()
.. autoclass:: InputMediaPhoto()
.. autoclass:: InputMediaVideo()
.. autoclass:: InputMediaAudio()
.. autoclass:: InputMediaAnimation()
.. autoclass:: InputMediaDocument()
.. autoclass:: InputPhoneContact()

..  Inline Mode
    -----------

.. autoclass:: InlineQuery()
.. autoclass:: InlineQueryResult()
.. autoclass:: InlineQueryResultArticle()

..  InputMessageContent
    -------------------

.. autoclass:: InputMessageContent()
.. autoclass:: InputTextMessageContent()

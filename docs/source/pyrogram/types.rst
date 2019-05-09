Types
=====

All Pyrogram types listed here are accessible through the main package directly.

**Example:**

.. code-block:: python

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
    :members:

.. autoclass:: UserStatus()
    :members:

.. autoclass:: Chat()
    :members:

.. autoclass:: ChatPreview()
    :members:

.. autoclass:: ChatPhoto()
    :members:

.. autoclass:: ChatMember()
    :members:

.. autoclass:: ChatMembers()
    :members:

.. autoclass:: ChatPermissions()
    :members:

.. autoclass:: Dialog()
    :members:

.. autoclass:: Dialogs()
    :members:

..  Messages & Media
    ----------------

.. autoclass:: Message()
    :members:

.. autoclass:: Messages()
    :members:

.. autoclass:: MessageEntity()
    :members:

.. autoclass:: Photo()
    :members:

.. autoclass:: PhotoSize()
    :members:

.. autoclass:: UserProfilePhotos()
    :members:

.. autoclass:: Audio()
    :members:

.. autoclass:: Document()
    :members:

.. autoclass:: Animation()
    :members:

.. autoclass:: Video()
    :members:

.. autoclass:: Voice()
    :members:

.. autoclass:: VideoNote()
    :members:

.. autoclass:: Contact()
    :members:

.. autoclass:: Location()
    :members:

.. autoclass:: Venue()
    :members:

.. autoclass:: Sticker()
    :members:

.. autoclass:: Game()
    :members:

.. autoclass:: Poll()
    :members:

.. autoclass:: PollOption()
    :members:

..  Keyboards
    ---------

.. autoclass:: ReplyKeyboardMarkup()
    :members:

.. autoclass:: KeyboardButton()
    :members:

.. autoclass:: ReplyKeyboardRemove()
    :members:

.. autoclass:: InlineKeyboardMarkup()
    :members:

.. autoclass:: InlineKeyboardButton()
    :members:

.. autoclass:: ForceReply()
    :members:

.. autoclass:: CallbackQuery()
    :members:

.. autoclass:: GameHighScore()
    :members:

.. autoclass:: CallbackGame()
    :members:

..  Input Media
    -----------

.. autoclass:: InputMedia()
    :members:

.. autoclass:: InputMediaPhoto()
    :members:

.. autoclass:: InputMediaVideo()
    :members:

.. autoclass:: InputMediaAudio()
    :members:

.. autoclass:: InputMediaAnimation()
    :members:

.. autoclass:: InputMediaDocument()
    :members:

.. autoclass:: InputPhoneContact()
    :members:


..  Inline Mode
    -----------

.. autoclass:: InlineQuery()
    :members:

.. autoclass:: InlineQueryResult()
    :members:

.. autoclass:: InlineQueryResultArticle()
    :members:

..  InputMessageContent
    -------------------

.. autoclass:: InputMessageContent()
    :members:

.. autoclass:: InputTextMessageContent()
    :members:

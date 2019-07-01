Bound Methods
=============

Some Pyrogram types define what are called bound methods. Bound methods are functions attached to a class which are
accessed via an instance of that class. They make it even easier to call specific methods by automatically inferring
some of the required arguments.

.. code-block:: python
    :emphasize-lines: 8

    from pyrogram import Client

    app = Client("my_account")


    @app.on_message()
    def hello(client, message)
        message.reply("hi")


    app.run()

.. currentmodule:: pyrogram

Index
-----

Message
^^^^^^^

.. hlist::
    :columns: 3

    - :meth:`~Message.click`
    - :meth:`~Message.delete`
    - :meth:`~Message.download`
    - :meth:`~Message.forward`
    - :meth:`~Message.pin`
    - :meth:`~Message.edit_text`
    - :meth:`~Message.edit_caption`
    - :meth:`~Message.edit_media`
    - :meth:`~Message.edit_reply_markup`
    - :meth:`~Message.reply_text`
    - :meth:`~Message.reply_animation`
    - :meth:`~Message.reply_audio`
    - :meth:`~Message.reply_cached_media`
    - :meth:`~Message.reply_chat_action`
    - :meth:`~Message.reply_contact`
    - :meth:`~Message.reply_document`
    - :meth:`~Message.reply_game`
    - :meth:`~Message.reply_inline_bot_result`
    - :meth:`~Message.reply_location`
    - :meth:`~Message.reply_media_group`
    - :meth:`~Message.reply_photo`
    - :meth:`~Message.reply_poll`
    - :meth:`~Message.reply_sticker`
    - :meth:`~Message.reply_venue`
    - :meth:`~Message.reply_video`
    - :meth:`~Message.reply_video_note`
    - :meth:`~Message.reply_voice`

Chat
^^^^

.. hlist::
    :columns: 2

    - :meth:`~Chat.archive`
    - :meth:`~Chat.unarchive`
    - :meth:`~Chat.set_title`
    - :meth:`~Chat.set_description`
    - :meth:`~Chat.set_photo`
    - :meth:`~Chat.kick_member`
    - :meth:`~Chat.unban_member`
    - :meth:`~Chat.restrict_member`
    - :meth:`~Chat.promote_member`

User
^^^^

.. hlist::
    :columns: 2

    - :meth:`~User.archive`
    - :meth:`~User.unarchive`

CallbackQuery
^^^^^^^^^^^^^

.. hlist::
    :columns: 3

    - :meth:`~CallbackQuery.answer`
    - :meth:`~CallbackQuery.edit_message_text`
    - :meth:`~CallbackQuery.edit_message_caption`
    - :meth:`~CallbackQuery.edit_message_media`
    - :meth:`~CallbackQuery.edit_message_reply_markup`

InlineQuery
^^^^^^^^^^^

.. hlist::
    :columns: 2

    - :meth:`~InlineQuery.answer`

-----

Details
-------

.. Message
.. automethod:: Message.click()
.. automethod:: Message.delete()
.. automethod:: Message.download()
.. automethod:: Message.forward()
.. automethod:: Message.pin()
.. automethod:: Message.edit_text()
.. automethod:: Message.edit_caption()
.. automethod:: Message.edit_media()
.. automethod:: Message.edit_reply_markup()
.. automethod:: Message.reply_text()
.. automethod:: Message.reply_animation()
.. automethod:: Message.reply_audio()
.. automethod:: Message.reply_cached_media()
.. automethod:: Message.reply_chat_action()
.. automethod:: Message.reply_contact()
.. automethod:: Message.reply_document()
.. automethod:: Message.reply_game()
.. automethod:: Message.reply_inline_bot_result()
.. automethod:: Message.reply_location()
.. automethod:: Message.reply_media_group()
.. automethod:: Message.reply_photo()
.. automethod:: Message.reply_poll()
.. automethod:: Message.reply_sticker()
.. automethod:: Message.reply_venue()
.. automethod:: Message.reply_video()
.. automethod:: Message.reply_video_note()
.. automethod:: Message.reply_voice()

.. Chat
.. automethod:: Chat.archive()
.. automethod:: Chat.unarchive()
.. automethod:: Chat.set_title()
.. automethod:: Chat.set_description()
.. automethod:: Chat.set_photo()
.. automethod:: Chat.kick_member()
.. automethod:: Chat.unban_member()
.. automethod:: Chat.restrict_member()
.. automethod:: Chat.promote_member()

.. User
.. automethod:: User.archive()
.. automethod:: User.unarchive()

.. CallbackQuery
.. automethod:: CallbackQuery.answer()
.. automethod:: CallbackQuery.edit_message_text()
.. automethod:: CallbackQuery.edit_message_caption()
.. automethod:: CallbackQuery.edit_message_media()
.. automethod:: CallbackQuery.edit_message_reply_markup()

.. InlineQuery
.. automethod:: InlineQuery.answer()

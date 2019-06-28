Available Methods
=================

This page is about Pyrogram methods. All the methods listed here are bound to a :class:`~pyrogram.Client` instance.

.. code-block:: python
    :emphasize-lines: 6

    from pyrogram import Client

    app = Client("my_account")

    with app:
        app.send_message("haskell", "hi")

.. currentmodule:: pyrogram

Index
-----

Utilities
^^^^^^^^^

.. hlist::
    :columns: 4

    - :meth:`~Client.start`
    - :meth:`~Client.stop`
    - :meth:`~Client.restart`
    - :meth:`~Client.idle`
    - :meth:`~Client.run`
    - :meth:`~Client.add_handler`
    - :meth:`~Client.remove_handler`
    - :meth:`~Client.stop_transmission`
    - :meth:`~Client.export_session_string`

Messages
^^^^^^^^

.. hlist::
    :columns: 3

    - :meth:`~Client.send_message`
    - :meth:`~Client.forward_messages`
    - :meth:`~Client.send_photo`
    - :meth:`~Client.send_audio`
    - :meth:`~Client.send_document`
    - :meth:`~Client.send_sticker`
    - :meth:`~Client.send_animated_sticker`
    - :meth:`~Client.send_video`
    - :meth:`~Client.send_animation`
    - :meth:`~Client.send_voice`
    - :meth:`~Client.send_video_note`
    - :meth:`~Client.send_media_group`
    - :meth:`~Client.send_location`
    - :meth:`~Client.send_venue`
    - :meth:`~Client.send_contact`
    - :meth:`~Client.send_cached_media`
    - :meth:`~Client.edit_message_text`
    - :meth:`~Client.edit_message_caption`
    - :meth:`~Client.edit_message_media`
    - :meth:`~Client.edit_message_reply_markup`
    - :meth:`~Client.edit_inline_text`
    - :meth:`~Client.edit_inline_caption`
    - :meth:`~Client.edit_inline_media`
    - :meth:`~Client.edit_inline_reply_markup`
    - :meth:`~Client.send_chat_action`
    - :meth:`~Client.delete_messages`
    - :meth:`~Client.get_messages`
    - :meth:`~Client.get_history`
    - :meth:`~Client.get_history_count`
    - :meth:`~Client.read_history`
    - :meth:`~Client.iter_history`
    - :meth:`~Client.send_poll`
    - :meth:`~Client.vote_poll`
    - :meth:`~Client.stop_poll`
    - :meth:`~Client.retract_vote`
    - :meth:`~Client.download_media`

Chats
^^^^^

.. hlist::
    :columns: 3

    - :meth:`~Client.join_chat`
    - :meth:`~Client.leave_chat`
    - :meth:`~Client.kick_chat_member`
    - :meth:`~Client.unban_chat_member`
    - :meth:`~Client.restrict_chat_member`
    - :meth:`~Client.promote_chat_member`
    - :meth:`~Client.export_chat_invite_link`
    - :meth:`~Client.set_chat_photo`
    - :meth:`~Client.delete_chat_photo`
    - :meth:`~Client.set_chat_title`
    - :meth:`~Client.set_chat_description`
    - :meth:`~Client.pin_chat_message`
    - :meth:`~Client.unpin_chat_message`
    - :meth:`~Client.get_chat`
    - :meth:`~Client.get_chat_member`
    - :meth:`~Client.get_chat_members`
    - :meth:`~Client.get_chat_members_count`
    - :meth:`~Client.iter_chat_members`
    - :meth:`~Client.get_dialogs`
    - :meth:`~Client.iter_dialogs`
    - :meth:`~Client.get_dialogs_count`
    - :meth:`~Client.restrict_chat`
    - :meth:`~Client.update_chat_username`
    - :meth:`~Client.archive_chats`
    - :meth:`~Client.unarchive_chats`

Users
^^^^^

.. hlist::
    :columns: 3

    - :meth:`~Client.get_me`
    - :meth:`~Client.get_users`
    - :meth:`~Client.get_profile_photos`
    - :meth:`~Client.get_profile_photos_count`
    - :meth:`~Client.iter_profile_photos`
    - :meth:`~Client.set_profile_photo`
    - :meth:`~Client.delete_profile_photos`
    - :meth:`~Client.update_username`
    - :meth:`~Client.get_user_dc`
    - :meth:`~Client.block_user`
    - :meth:`~Client.unblock_user`

Contacts
^^^^^^^^

.. hlist::
    :columns: 3

    - :meth:`~Client.add_contacts`
    - :meth:`~Client.get_contacts`
    - :meth:`~Client.get_contacts_count`
    - :meth:`~Client.delete_contacts`

Password
^^^^^^^^

.. hlist::
    :columns: 3

    - :meth:`~Client.enable_cloud_password`
    - :meth:`~Client.change_cloud_password`
    - :meth:`~Client.remove_cloud_password`

Bots
^^^^

.. hlist::
    :columns: 3

    - :meth:`~Client.get_inline_bot_results`
    - :meth:`~Client.send_inline_bot_result`
    - :meth:`~Client.answer_callback_query`
    - :meth:`~Client.answer_inline_query`
    - :meth:`~Client.request_callback_answer`
    - :meth:`~Client.send_game`
    - :meth:`~Client.set_game_score`
    - :meth:`~Client.get_game_high_scores`

Advanced Usage (Raw API)
^^^^^^^^^^^^^^^^^^^^^^^^

Learn more about these methods at :doc:`Advanced Usage <../topics/advanced-usage>`.

.. hlist::
    :columns: 4

    - :meth:`~Client.send`
    - :meth:`~Client.resolve_peer`
    - :meth:`~Client.save_file`

-----

Details
-------

..  Utilities
.. automethod:: Client.start()
.. automethod:: Client.stop()
.. automethod:: Client.restart()
.. automethod:: Client.idle()
.. automethod:: Client.run()
.. automethod:: Client.add_handler()
.. automethod:: Client.remove_handler()
.. automethod:: Client.stop_transmission()
.. automethod:: Client.export_session_string()

..  Messages
.. automethod:: Client.send_message()
.. automethod:: Client.forward_messages()
.. automethod:: Client.send_photo()
.. automethod:: Client.send_audio()
.. automethod:: Client.send_document()
.. automethod:: Client.send_sticker()
.. automethod:: Client.send_animated_sticker()
.. automethod:: Client.send_video()
.. automethod:: Client.send_animation()
.. automethod:: Client.send_voice()
.. automethod:: Client.send_video_note()
.. automethod:: Client.send_media_group()
.. automethod:: Client.send_location()
.. automethod:: Client.send_venue()
.. automethod:: Client.send_contact()
.. automethod:: Client.send_cached_media()
.. automethod:: Client.send_chat_action()
.. automethod:: Client.edit_message_text()
.. automethod:: Client.edit_message_caption()
.. automethod:: Client.edit_message_media()
.. automethod:: Client.edit_message_reply_markup()
.. automethod:: Client.edit_inline_text()
.. automethod:: Client.edit_inline_caption()
.. automethod:: Client.edit_inline_media()
.. automethod:: Client.edit_inline_reply_markup()
.. automethod:: Client.delete_messages()
.. automethod:: Client.get_messages()
.. automethod:: Client.get_history()
.. automethod:: Client.get_history_count()
.. automethod:: Client.read_history()
.. automethod:: Client.iter_history()
.. automethod:: Client.send_poll()
.. automethod:: Client.vote_poll()
.. automethod:: Client.stop_poll()
.. automethod:: Client.retract_vote()
.. automethod:: Client.download_media()

..  Chats
.. automethod:: Client.join_chat()
.. automethod:: Client.leave_chat()
.. automethod:: Client.kick_chat_member()
.. automethod:: Client.unban_chat_member()
.. automethod:: Client.restrict_chat_member()
.. automethod:: Client.promote_chat_member()
.. automethod:: Client.export_chat_invite_link()
.. automethod:: Client.set_chat_photo()
.. automethod:: Client.delete_chat_photo()
.. automethod:: Client.set_chat_title()
.. automethod:: Client.set_chat_description()
.. automethod:: Client.pin_chat_message()
.. automethod:: Client.unpin_chat_message()
.. automethod:: Client.get_chat()
.. automethod:: Client.get_chat_member()
.. automethod:: Client.get_chat_members()
.. automethod:: Client.get_chat_members_count()
.. automethod:: Client.iter_chat_members()
.. automethod:: Client.get_dialogs()
.. automethod:: Client.iter_dialogs()
.. automethod:: Client.get_dialogs_count()
.. automethod:: Client.restrict_chat()
.. automethod:: Client.update_chat_username()
.. automethod:: Client.archive_chats()
.. automethod:: Client.unarchive_chats()

..  Users
.. automethod:: Client.get_me()
.. automethod:: Client.get_users()
.. automethod:: Client.get_profile_photos()
.. automethod:: Client.get_profile_photos_count()
.. automethod:: Client.iter_profile_photos()
.. automethod:: Client.set_profile_photo()
.. automethod:: Client.delete_profile_photos()
.. automethod:: Client.update_username()
.. automethod:: Client.get_user_dc()
.. automethod:: Client.block_user()
.. automethod:: Client.unblock_user()

..  Contacts
.. automethod:: Client.add_contacts()
.. automethod:: Client.get_contacts()
.. automethod:: Client.get_contacts_count()
.. automethod:: Client.delete_contacts()

..  Password
.. automethod:: Client.enable_cloud_password()
.. automethod:: Client.change_cloud_password()
.. automethod:: Client.remove_cloud_password()

..  Bots
.. automethod:: Client.get_inline_bot_results()
.. automethod:: Client.send_inline_bot_result()
.. automethod:: Client.answer_callback_query()
.. automethod:: Client.answer_inline_query()
.. automethod:: Client.request_callback_answer()
.. automethod:: Client.send_game()
.. automethod:: Client.set_game_score()
.. automethod:: Client.get_game_high_scores()

.. Advanced Usage
.. automethod:: Client.send()
.. automethod:: Client.resolve_peer()
.. automethod:: Client.save_file()
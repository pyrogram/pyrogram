Available Methods
=================

All Pyrogram methods listed here are bound to a :obj:`Client <pyrogram.Client>` instance.

**Example:**

.. code-block:: python

    from pyrogram import Client

    app = Client(...)

    with app:
        app.send_message("haskell", "hi")

.. currentmodule:: pyrogram.Client

Utilities
---------

.. autosummary::
    :nosignatures:

    start
    stop
    restart
    idle
    run
    add_handler
    remove_handler
    send
    resolve_peer
    save_file
    stop_transmission

Messages
--------

.. autosummary::
    :nosignatures:

    send_message
    forward_messages
    send_photo
    send_audio
    send_document
    send_sticker
    send_video
    send_animation
    send_voice
    send_video_note
    send_media_group
    send_location
    send_venue
    send_contact
    send_cached_media
    send_chat_action
    edit_message_text
    edit_message_caption
    edit_message_reply_markup
    edit_message_media
    delete_messages
    get_messages
    get_history
    get_history_count
    iter_history
    send_poll
    vote_poll
    stop_poll
    retract_vote
    download_media

Chats
-----

.. autosummary::
    :nosignatures:

    join_chat
    leave_chat
    kick_chat_member
    unban_chat_member
    restrict_chat_member
    promote_chat_member
    export_chat_invite_link
    set_chat_photo
    delete_chat_photo
    set_chat_title
    set_chat_description
    pin_chat_message
    unpin_chat_message
    get_chat
    get_chat_preview
    get_chat_member
    get_chat_members
    get_chat_members_count
    iter_chat_members
    get_dialogs
    iter_dialogs
    get_dialogs_count
    restrict_chat
    update_chat_username

Users
-----

.. autosummary::
    :nosignatures:

    get_me
    get_users
    get_user_profile_photos
    get_user_profile_photos_count
    set_user_profile_photo
    delete_user_profile_photos
    update_username

Contacts
--------

.. autosummary::
    :nosignatures:

    add_contacts
    get_contacts
    get_contacts_count
    delete_contacts

Password
--------

.. autosummary::
    :nosignatures:

    enable_cloud_password
    change_cloud_password
    remove_cloud_password

Bots
----

.. autosummary::
    :nosignatures:

    get_inline_bot_results
    send_inline_bot_result
    answer_callback_query
    answer_inline_query
    request_callback_answer
    send_game
    set_game_score
    get_game_high_scores
    answer_inline_query

..  Utilities
    ---------

.. automethod:: pyrogram.Client.start()
.. automethod:: pyrogram.Client.stop()
.. automethod:: pyrogram.Client.restart()
.. automethod:: pyrogram.Client.idle()
.. automethod:: pyrogram.Client.run()
.. automethod:: pyrogram.Client.add_handler()
.. automethod:: pyrogram.Client.remove_handler()
.. automethod:: pyrogram.Client.send()
.. automethod:: pyrogram.Client.resolve_peer()
.. automethod:: pyrogram.Client.save_file()
.. automethod:: pyrogram.Client.stop_transmission()

..  Messages
    --------

.. automethod:: pyrogram.Client.send_message()
.. automethod:: pyrogram.Client.forward_messages()
.. automethod:: pyrogram.Client.send_photo()
.. automethod:: pyrogram.Client.send_audio()
.. automethod:: pyrogram.Client.send_document()
.. automethod:: pyrogram.Client.send_sticker()
.. automethod:: pyrogram.Client.send_video()
.. automethod:: pyrogram.Client.send_animation()
.. automethod:: pyrogram.Client.send_voice()
.. automethod:: pyrogram.Client.send_video_note()
.. automethod:: pyrogram.Client.send_media_group()
.. automethod:: pyrogram.Client.send_location()
.. automethod:: pyrogram.Client.send_venue()
.. automethod:: pyrogram.Client.send_contact()
.. automethod:: pyrogram.Client.send_cached_media()
.. automethod:: pyrogram.Client.send_chat_action()
.. automethod:: pyrogram.Client.edit_message_text()
.. automethod:: pyrogram.Client.edit_message_caption()
.. automethod:: pyrogram.Client.edit_message_reply_markup()
.. automethod:: pyrogram.Client.edit_message_media()
.. automethod:: pyrogram.Client.delete_messages()
.. automethod:: pyrogram.Client.get_messages()
.. automethod:: pyrogram.Client.get_history()
.. automethod:: pyrogram.Client.get_history_count()
.. automethod:: pyrogram.Client.iter_history()
.. automethod:: pyrogram.Client.send_poll()
.. automethod:: pyrogram.Client.vote_poll()
.. automethod:: pyrogram.Client.stop_poll()
.. automethod:: pyrogram.Client.retract_vote()
.. automethod:: pyrogram.Client.download_media()

..  Chats
    -----

.. automethod:: pyrogram.Client.join_chat()
.. automethod:: pyrogram.Client.leave_chat()
.. automethod:: pyrogram.Client.kick_chat_member()
.. automethod:: pyrogram.Client.unban_chat_member()
.. automethod:: pyrogram.Client.restrict_chat_member()
.. automethod:: pyrogram.Client.promote_chat_member()
.. automethod:: pyrogram.Client.export_chat_invite_link()
.. automethod:: pyrogram.Client.set_chat_photo()
.. automethod:: pyrogram.Client.delete_chat_photo()
.. automethod:: pyrogram.Client.set_chat_title()
.. automethod:: pyrogram.Client.set_chat_description()
.. automethod:: pyrogram.Client.pin_chat_message()
.. automethod:: pyrogram.Client.unpin_chat_message()
.. automethod:: pyrogram.Client.get_chat()
.. automethod:: pyrogram.Client.get_chat_preview()
.. automethod:: pyrogram.Client.get_chat_member()
.. automethod:: pyrogram.Client.get_chat_members()
.. automethod:: pyrogram.Client.get_chat_members_count()
.. automethod:: pyrogram.Client.iter_chat_members()
.. automethod:: pyrogram.Client.get_dialogs()
.. automethod:: pyrogram.Client.iter_dialogs()
.. automethod:: pyrogram.Client.get_dialogs_count()
.. automethod:: pyrogram.Client.restrict_chat()
.. automethod:: pyrogram.Client.update_chat_username()

..  Users
    -----

.. automethod:: pyrogram.Client.get_me()
.. automethod:: pyrogram.Client.get_users()
.. automethod:: pyrogram.Client.get_user_profile_photos()
.. automethod:: pyrogram.Client.get_user_profile_photos_count()
.. automethod:: pyrogram.Client.set_user_profile_photo()
.. automethod:: pyrogram.Client.delete_user_profile_photos()
.. automethod:: pyrogram.Client.update_username()

..  Contacts
    --------

.. automethod:: pyrogram.Client.add_contacts()
.. automethod:: pyrogram.Client.get_contacts()
.. automethod:: pyrogram.Client.get_contacts_count()
.. automethod:: pyrogram.Client.delete_contacts()

..  Password
    --------

.. automethod:: pyrogram.Client.enable_cloud_password()
.. automethod:: pyrogram.Client.change_cloud_password()
.. automethod:: pyrogram.Client.remove_cloud_password()

..  Bots
    ----

.. automethod:: pyrogram.Client.get_inline_bot_results()
.. automethod:: pyrogram.Client.send_inline_bot_result()
.. automethod:: pyrogram.Client.answer_callback_query()
.. automethod:: pyrogram.Client.answer_inline_query()
.. automethod:: pyrogram.Client.request_callback_answer()
.. automethod:: pyrogram.Client.send_game()
.. automethod:: pyrogram.Client.set_game_score()
.. automethod:: pyrogram.Client.get_game_high_scores()
.. automethod:: pyrogram.Client.answer_inline_query()
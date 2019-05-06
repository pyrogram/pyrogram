Client
======

.. currentmodule:: pyrogram.Client

.. autoclass:: pyrogram.Client

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

Decorators
----------

.. autosummary::
    :nosignatures:

    on_message
    on_callback_query
    on_inline_query
    on_deleted_messages
    on_user_status
    on_disconnect
    on_raw_update

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
    set_user_profile_photo
    delete_user_profile_photos
    update_username

Contacts
--------

.. autosummary::
    :nosignatures:

    add_contacts
    get_contacts
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


.. autoclass:: pyrogram.Client
    :inherited-members:
    :members:

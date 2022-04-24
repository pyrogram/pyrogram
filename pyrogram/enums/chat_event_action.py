#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-present Dan <https://github.com/delivrance>
#
#  This file is part of Pyrogram.
#
#  Pyrogram is free software: you can redistribute it and/or modify
#  it under the terms of the GNU Lesser General Public License as published
#  by the Free Software Foundation, either version 3 of the License, or
#  (at your option) any later version.
#
#  Pyrogram is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU Lesser General Public License for more details.
#
#  You should have received a copy of the GNU Lesser General Public License
#  along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from enum import auto

from .auto_name import AutoName


class ChatEventAction(AutoName):
    """Chat event action enumeration used in :meth:`~pyrogram.Client.get_chat_event_log`."""

    DESCRIPTION_CHANGED = auto()
    "The chat description has been changed (see ``old_description`` and ``new_description``)"

    HISTORY_TTL_CHANGED = auto()
    "The history time-to-live has been changed (see ``old_history_ttl`` and ``new_history_ttl``)"

    LINKED_CHAT_CHANGED = auto()
    "The linked chat has been changed (see ``old_linked_chat`` and ``new_linked_chat``)"

    # LOCATION_CHANGED = auto()
    ""

    PHOTO_CHANGED = auto()
    "The chat photo has been changed (see ``old_photo`` and ``new_photo``)"

    # STICKER_SET_CHANGED = auto()
    ""

    TITLE_CHANGED = auto()
    "the chat title has been changed (see ``old_title`` and ``new_title``)"

    USERNAME_CHANGED = auto()
    "the chat username has been changed (see ``old_username`` and ``new_username``)"

    CHAT_PERMISSIONS_CHANGED = auto()
    "the default chat permissions has been changed (see ``old_chat_permissions`` and ``new_chat_permissions``)"

    MESSAGE_DELETED = auto()
    "a message has been deleted (see ``deleted_message``)"

    # VOICE_CHAT_DISCARDED = auto()
    ""

    MESSAGE_EDITED = auto()
    "a message has been edited (see ``old_message`` and ``new_message``)"

    INVITE_LINK_EDITED = auto()
    "An invite link has been edited (see ``old_invite_link`` and ``new_invite`` link)"

    INVITE_LINK_REVOKED = auto()
    "An invite link has been revoked (see ``revoked_invite_link``)"

    INVITE_LINK_DELETED = auto()
    "An invite link has been deleted (see ``deleted_invite_link``)"

    MEMBER_INVITED = auto()
    "a member has been invited by someone (see ``invited_member``)"

    MEMBER_JOINED = auto()
    "a member joined by themselves. (see ``user``)"

    # MEMBER_JOINED_BY_LINK = auto()
    ""

    MEMBER_LEFT = auto()
    "a member left by themselves. (see ``user``)"

    # MEMBER_MUTED = auto()
    ""

    ADMINISTRATOR_PRIVILEGES_CHANGED = auto()
    "a chat member has been promoted/demoted or their administrator privileges has changed (see ``old_administrator_privileges`` and ``new_administrator_privileges``)"

    MEMBER_PERMISSIONS_CHANGED = auto()
    "a chat member has been restricted/unrestricted or banned/unbanned, or their permissions has changed (see ``old_member_permissions`` and ``new_member_permissions``)"

    # MEMBER_UNMUTED = auto()
    ""

    # MEMBER_VOLUME_CHANGED = auto()
    ""

    # VIDEO_CHAT_STARTED = auto()
    ""

    POLL_STOPPED = auto()
    "a poll has been stopped (see ``stopped_poll``)"

    # VOICE_CHAT_SETTINGS_CHANGED = auto()
    ""

    INVITES_ENABLED = auto()
    "the chat invitation has been enabled or disabled (see ``invites_enabled``)"

    HISTORY_HIDDEN = auto()
    "the chat history has been hidden or unhidden (see ``history_hidden``)"

    SIGNATURES_ENABLED = auto()
    "the message signatures have been enabled or disabled (see ``signatures_enabled``)"

    SLOW_MODE_CHANGED = auto()
    "the slow mode has been changes (see ``old_slow_mode`` and ``new_slow_mode``)"

    MESSAGE_PINNED = auto()
    "a message has been pinned (see ``pinned_message``)"

    MESSAGE_UNPINNED = auto()
    "a message has been unpinned (see ``unpinned_message``)"

    UNKNOWN = auto()
    "Unknown chat event action"

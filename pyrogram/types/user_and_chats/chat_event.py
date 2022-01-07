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

from enum import Enum, auto
from typing import List, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types
from ..object import Object


class AutoName(Enum):
    def _generate_next_value_(self, *args):
        return self.lower()


class ChatEventAction(AutoName):
    DESCRIPTION_CHANGED = auto()
    HISTORY_TTL_CHANGED = auto()
    LINKED_CHAT_CHANGED = auto()
    # LOCATION_CHANGED = auto()
    PHOTO_CHANGED = auto()
    # STICKER_SET_CHANGED = auto()
    TITLE_CHANGED = auto()
    USERNAME_CHANGED = auto()
    CHAT_PERMISSIONS_CHANGED = auto()
    MESSAGE_DELETED = auto()
    # VOICE_CHAT_DISCARDED = auto()
    MESSAGE_EDITED = auto()
    INVITE_LINK_EDITED = auto()
    INVITE_LINK_REVOKED = auto()
    INVITE_LINK_DELETED = auto()
    MEMBER_INVITED = auto()
    MEMBER_JOINED = auto()
    # MEMBER_JOINED_BY_LINK = auto()
    MEMBER_LEFT = auto()
    # MEMBER_MUTED = auto()
    ADMIN_RIGHTS_CHANGED = auto()
    MEMBER_PERMISSIONS_CHANGED = auto()
    # MEMBER_UNMUTED = auto()
    # MEMBER_VOLUME_CHANGED = auto()
    # VOICE_CHAT_STARTED = auto()
    POLL_STOPPED = auto()
    # VOICE_CHAT_SETTINGS_CHANGED = auto()
    INVITES_ENABLED = auto()
    HISTORY_HIDDEN = auto()
    SIGNATURES_ENABLED = auto()
    SLOW_MODE_CHANGED = auto()
    MESSAGE_PINNED = auto()
    MESSAGE_UNPINNED = auto()
    UNKNOWN = auto()


class ChatEvent(Object):
    """A chat event from the recent actions log (also known as admin log).

    Parameters:
        id (``int``):
            Chat event identifier.

        date (``int``):
            Date of the event. Unix time.

        action (``str``):
            Event action. Can be:

            - "description_changed": the chat description has been changed
              (see *old_description* and *new_description* below).

            - "history_ttl_changed": the history time-to-live has been changed
              (see *old_history_ttl* and *new_history_ttl* below).

            - "linked_chat_changed": the linked chat has been changed
              (see *old_linked_chat* and *new_linked_chat* below).

            - "photo_changed": the chat photo has been changed
              (see *old_photo* and *new_photo* below).

            - "title_changed": the chat title has been changed
              (see *old_title* and *new_title* below).

            - "username_changed": the chat username has been changed
              (see *old_username* and *new_username* below).

            - "chat_permissions_changed": the default chat permissions has been changed
              (see *old_chat_permissions* and *new_chat_permissions* below).

            - "message_deleted": a message has been deleted
              (see *deleted_message* below).

            - "message_edited": a message has been edited
              (see *old_message* and *new_message* below).

            - "member_invited": a member has been invited by someone
              (see *invited_member* below).

            - "member_joined": a member joined by themselves.
              (see *user* below)

            - "member_left": a member left by themselves.
              (see *user* below).

            - "admin_rights_changed": a chat member has been promoted/demoted or their administrator rights has changed
              (see *old_admin_rights* and *new_admin_rights* below).

            - "member_permissions_changed": a chat member has been restricted/unrestricted or banned/unbanned, or their
              permissions has changed (see *old_member_permissions* and *new_member_permissions* below).

            - "poll_stopped": a poll has been stopped
              (see *stopped_poll* below).

            - "invites_enabled": the chat invitation has been enabled or disabled
              (see *invites_enabled* below).

            - "history_hidden": the chat history has been hidden or unhidden
              (see *history_hidden* below).

            - "signatures_enabled": the message signatures have been enabled or disabled
              (see *signatures_enabled* below).

            - "slow_mode_changed": the slow mode has been changes
              (see *old_slow_mode* and *new_slow_mode* below).

            - "message_pinned": a message has been pinned
              (see *pinned_message* below).

            - "message_unpinned": a message has been unpinned
              (see *unpinned_message* below).

            - "invite_link_edited": an invite link has been edited
              (see *edited_invite_link* below).

            - "invite_link_revoked": an invite link has been revoked
              (see *revoked_invite_link* below).

            - "invite_link_deleted": an invite link has been deleted
              (see *deleted_invite_link* below).

        user (:obj:`~pyrogram.types.User`):
            User that triggered the event.

        old_description, new_description (``str``, *optional*):
            Previous and new chat description.
            For "description_changed" only.

        old_history_ttl, new_history_ttl (``int``, *optional*):
            Previous and new chat history TTL.
            For "history_ttl_changed" only.

        old_linked_chat, new_linked_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Previous and new linked chat.
            For "linked_chat_changed" only.

        old_photo, new_photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Previous and new chat photo.
            For "photo_changed" only.

        old_title, new_title (``str``, *optional*):
            Previous and new chat title.
            For "title_changed" only.

        old_username, new_username (``str``, *optional*):
            Previous and new chat username.
            For "username_changed" only.

        old_chat_permissions, new_chat_permissions (:obj:`~pyrogram.types.ChatPermissions`, *optional*):
            Previous and new default chat permissions.
            For "chat_permissions_changed" only.

        deleted_message (:obj:`~pyrogram.types.Message`, *optional*):
            Deleted message.
            For "deleted_message" only.

        old_message, new_message (:obj:`~pyrogram.types.Message`, *optional*):
            Previous and new message before it has been edited.
            For "message_edited" only.

        invited_member (:obj:`~pyrogram.types.ChatMember`, *optional*):
            New invited chat member.
            For "member_invited" only.

        old_admin_rights, new_admin_rights (:obj:`~pyrogram.types.ChatMember`, *optional*):
            Previous and new administrator rights.
            For "admin_rights_changed" only.

        old_member_permissions, new_member_permissions (:obj:`~pyrogram.types.ChatMember`, *optional*):
            Previous and new member permissions.
            For "member_permissions_changed" only.

        stopped_poll (:obj:`~pyrogram.types.Message`, *optional*):
            Message containing the stopped poll.
            For "poll_stopped" only.

        invites_enabled (``bool``, *optional*):
            If chat invites were enabled (True) or disabled (False).
            For "invites_enabled" only.

        history_hidden (``bool``, *optional*):
            If chat history has been hidden (True) or unhidden (False).
            For "history_hidden" only.

        signatures_enabled (``bool``, *optional*):
            If message signatures were enabled (True) or disabled (False).
            For "signatures_enabled" only.

        old_slow_mode, new_slow_mode (``int``, *optional*):
            Previous and new slow mode value in seconds.
            For "slow_mode_changed" only.

        pinned_message (:obj:`~pyrogram.types.Message`, *optional*):
            Pinned message.
            For "message_pinned" only.

        unpinned_message (:obj:`~pyrogram.types.Message`, *optional*):
            Unpinned message.
            For "unpinned_message" only.

        old_invite_link, new_invite_link (:obj:`~pyrogram.types.ChatInviteLink`, *optional*):
            Previous and new edited invite link.
            For "invite_link_edited" only.

        revoked_invite_link (:obj:`~pyrogram.types.ChatInviteLink`, *optional*):
            Revoked invite link.
            For "invite_link_revoked" only.

        deleted_invite_link (:obj:`~pyrogram.types.ChatInviteLink`, *optional*):
            Deleted invite link.
            For "invite_link_deleted" only.
    """

    def __init__(
        self, *,
        id: int,
        date: int,
        user: "types.User",
        action: str,

        old_description: str = None,
        new_description: str = None,

        old_history_ttl: int = None,
        new_history_ttl: int = None,

        old_linked_chat: "types.Chat" = None,
        new_linked_chat: "types.Chat" = None,

        old_photo: "types.Photo" = None,
        new_photo: "types.Photo" = None,

        old_title: str = None,
        new_title: str = None,

        old_username: str = None,
        new_username: str = None,

        old_chat_permissions: "types.ChatPermissions" = None,
        new_chat_permissions: "types.ChatPermissions" = None,

        deleted_message: "types.Message" = None,

        old_message: "types.Message" = None,
        new_message: "types.Message" = None,

        invited_member: "types.ChatMember" = None,

        old_admin_rights: "types.ChatMember" = None,
        new_admin_rights: "types.ChatMember" = None,

        old_member_permissions: "types.ChatMember" = None,
        new_member_permissions: "types.ChatMember" = None,

        stopped_poll: "types.Message" = None,

        invites_enabled: "types.ChatMember" = None,

        history_hidden: bool = None,

        signatures_enabled: bool = None,

        old_slow_mode: int = None,
        new_slow_mode: int = None,

        pinned_message: "types.Message" = None,
        unpinned_message: "types.Message" = None,

        old_invite_link: "types.ChatInviteLink" = None,
        new_invite_link: "types.ChatInviteLink" = None,
        revoked_invite_link: "types.ChatInviteLink" = None,
        deleted_invite_link: "types.ChatInviteLink" = None,
    ):
        super().__init__()

        self.id = id
        self.date = date
        self.action = action
        self.user = user

        self.old_description = old_description
        self.new_description = new_description

        self.old_history_ttl = old_history_ttl
        self.new_history_ttl = new_history_ttl

        self.old_linked_chat = old_linked_chat
        self.new_linked_chat = new_linked_chat

        self.old_photo = old_photo
        self.new_photo = new_photo

        self.old_title = old_title
        self.new_title = new_title

        self.old_username = old_username
        self.new_username = new_username

        self.old_chat_permissions = old_chat_permissions
        self.new_chat_permissions = new_chat_permissions

        self.deleted_message = deleted_message

        self.old_message = old_message
        self.new_message = new_message

        self.invited_member = invited_member

        self.old_admin_rights = old_admin_rights
        self.new_admin_rights = new_admin_rights

        self.old_member_permissions = old_member_permissions
        self.new_member_permissions = new_member_permissions

        self.stopped_poll = stopped_poll

        self.invites_enabled = invites_enabled

        self.history_hidden = history_hidden

        self.signatures_enabled = signatures_enabled

        self.old_slow_mode = old_slow_mode
        self.new_slow_mode = new_slow_mode

        self.pinned_message = pinned_message
        self.unpinned_message = unpinned_message

        self.old_invite_link = old_invite_link
        self.new_invite_link = new_invite_link
        self.revoked_invite_link = revoked_invite_link
        self.deleted_invite_link = deleted_invite_link

    @staticmethod
    async def _parse(
        client: "pyrogram.Client",
        event: "raw.base.ChannelAdminLogEvent",
        users: List["raw.base.User"],
        chats: List["raw.base.Chat"]
    ):
        users = {i.id: i for i in users}
        chats = {i.id: i for i in chats}

        user = types.User._parse(client, users[event.user_id])
        action = event.action

        old_description: Optional[str] = None
        new_description: Optional[str] = None

        old_history_ttl: Optional[int] = None
        new_history_ttl: Optional[int] = None

        old_linked_chat: Optional[types.Chat] = None
        new_linked_chat: Optional[types.Chat] = None

        old_photo: Optional[types.Photo] = None
        new_photo: Optional[types.Photo] = None

        old_title: Optional[str] = None
        new_title: Optional[str] = None

        old_username: Optional[str] = None
        new_username: Optional[str] = None

        old_chat_permissions: Optional[types.ChatPermissions] = None
        new_chat_permissions: Optional[types.ChatPermissions] = None

        deleted_message: Optional[types.Message] = None

        old_message: Optional[types.Message] = None
        new_message: Optional[types.Message] = None

        invited_member: Optional[types.ChatMember] = None

        old_admin_rights: Optional[types.ChatMember] = None
        new_admin_rights: Optional[types.ChatMember] = None

        old_member_permissions: Optional[types.ChatMember] = None
        new_member_permissions: Optional[types.ChatMember] = None

        stopped_poll: Optional[types.Message] = None

        invites_enabled: Optional[bool] = None

        history_hidden: Optional[bool] = None

        signatures_enabled: Optional[bool] = None

        old_slow_mode: Optional[int] = None
        new_slow_mode: Optional[int] = None

        pinned_message: Optional[types.Message] = None
        unpinned_message: Optional[types.Message] = None

        old_invite_link: Optional[types.ChatInviteLink] = None
        new_invite_link: Optional[types.ChatInviteLink] = None
        revoked_invite_link: Optional[types.ChatInviteLink] = None
        deleted_invite_link: Optional[types.ChatInviteLink] = None

        if isinstance(action, raw.types.ChannelAdminLogEventActionChangeAbout):
            old_description = action.prev_value
            new_description = action.new_value
            action = ChatEventAction.DESCRIPTION_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangeHistoryTTL):
            old_history_ttl = action.prev_value
            new_history_ttl = action.new_value
            action = ChatEventAction.HISTORY_TTL_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangeLinkedChat):
            old_linked_chat = types.Chat._parse_chat(client, chats[action.prev_value])
            new_linked_chat = types.Chat._parse_chat(client, chats[action.new_value])
            action = ChatEventAction.LINKED_CHAT_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangePhoto):
            old_photo = types.Photo._parse(client, action.prev_photo)
            new_photo = types.Photo._parse(client, action.new_photo)
            action = ChatEventAction.PHOTO_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangeTitle):
            old_title = action.prev_value
            new_title = action.new_value
            action = ChatEventAction.TITLE_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangeUsername):
            old_username = action.prev_value
            new_username = action.new_value
            action = ChatEventAction.USERNAME_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionDefaultBannedRights):
            old_chat_permissions = types.ChatPermissions._parse(action.prev_banned_rights)
            new_chat_permissions = types.ChatPermissions._parse(action.new_banned_rights)
            action = ChatEventAction.CHAT_PERMISSIONS_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionDeleteMessage):
            deleted_message = await types.Message._parse(client, action.message, users, chats)
            action = ChatEventAction.MESSAGE_DELETED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionEditMessage):
            old_message = await types.Message._parse(client, action.prev_message, users, chats)
            new_message = await types.Message._parse(client, action.new_message, users, chats)
            action = ChatEventAction.MESSAGE_EDITED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantInvite):
            invited_member = types.ChatMember._parse(client, action.participant, users, chats)
            action = ChatEventAction.MEMBER_INVITED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantToggleAdmin):
            old_admin_rights = types.ChatMember._parse(client, action.prev_participant, users, chats)
            new_admin_rights = types.ChatMember._parse(client, action.new_participant, users, chats)
            action = ChatEventAction.ADMIN_RIGHTS_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantToggleBan):
            old_member_permissions = types.ChatMember._parse(client, action.prev_participant, users, chats)
            new_member_permissions = types.ChatMember._parse(client, action.new_participant, users, chats)
            action = ChatEventAction.MEMBER_PERMISSIONS_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionStopPoll):
            stopped_poll = await types.Message._parse(client, action.message, users, chats)
            action = ChatEventAction.POLL_STOPPED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantJoin):
            action = ChatEventAction.MEMBER_JOINED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantLeave):
            action = ChatEventAction.MEMBER_LEFT.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionToggleInvites):
            invites_enabled = action.new_value
            action = ChatEventAction.INVITES_ENABLED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionTogglePreHistoryHidden):
            history_hidden = action.new_value
            action = ChatEventAction.HISTORY_HIDDEN.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionToggleSignatures):
            signatures_enabled = action.new_value
            action = ChatEventAction.SIGNATURES_ENABLED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionToggleSlowMode):
            old_slow_mode = action.prev_value
            new_slow_mode = action.new_value
            action = ChatEventAction.SLOW_MODE_CHANGED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionUpdatePinned):
            message = action.message

            if message.pinned:
                pinned_message = await types.Message._parse(client, message, users, chats)
                action = ChatEventAction.MESSAGE_PINNED.value
            else:
                unpinned_message = await types.Message._parse(client, message, users, chats)
                action = ChatEventAction.MESSAGE_UNPINNED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionExportedInviteEdit):
            old_invite_link = types.ChatInviteLink._parse(client, action.prev_invite, users)
            new_invite_link = types.ChatInviteLink._parse(client, action.new_invite, users)
            action = ChatEventAction.INVITE_LINK_EDITED.value

        elif isinstance(action, raw.types.ChannelAdminLogEventActionExportedInviteRevoke):
            revoked_invite_link = types.ChatInviteLink._parse(client, action.invite, users)
            action = ChatEventAction.INVITE_LINK_REVOKED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionExportedInviteDelete):
            deleted_invite_link = types.ChatInviteLink._parse(client, action.invite, users)
            action = ChatEventAction.INVITE_LINK_DELETED.value

        else:
            action = f"{ChatEventAction.UNKNOWN.value}-{action.QUALNAME}"

        return ChatEvent(
            id=event.id,
            date=event.date,
            user=user,
            action=action,
            old_description=old_description,
            new_description=new_description,

            old_history_ttl=old_history_ttl,
            new_history_ttl=new_history_ttl,

            old_linked_chat=old_linked_chat,
            new_linked_chat=new_linked_chat,

            old_photo=old_photo,
            new_photo=new_photo,

            old_title=old_title,
            new_title=new_title,

            old_username=old_username,
            new_username=new_username,

            old_chat_permissions=old_chat_permissions,
            new_chat_permissions=new_chat_permissions,

            deleted_message=deleted_message,

            old_message=old_message,
            new_message=new_message,

            invited_member=invited_member,

            old_admin_rights=old_admin_rights,
            new_admin_rights=new_admin_rights,

            old_member_permissions=old_member_permissions,
            new_member_permissions=new_member_permissions,

            stopped_poll=stopped_poll,

            invites_enabled=invites_enabled,

            history_hidden=history_hidden,

            signatures_enabled=signatures_enabled,

            old_slow_mode=old_slow_mode,
            new_slow_mode=new_slow_mode,

            pinned_message=pinned_message,
            unpinned_message=unpinned_message,

            old_invite_link=old_invite_link,
            new_invite_link=new_invite_link,
            revoked_invite_link=revoked_invite_link,
            deleted_invite_link=deleted_invite_link
        )

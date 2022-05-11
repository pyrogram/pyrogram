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

from datetime import datetime
from typing import List, Optional

import pyrogram
from pyrogram import raw
from pyrogram import types, utils, enums
from ..object import Object


class ChatEvent(Object):
    """A chat event from the recent actions log (also known as admin log).

    See ``action`` to know which kind of event this is and the relative attributes to get the event content.

    Parameters:
        id (``int``):
            Chat event identifier.

        date (:py:obj:`~datetime.datetime`):
            Date of the event.

        action (:obj:`~pyrogram.enums.ChatEventAction`):
            Event action.

        user (:obj:`~pyrogram.types.User`):
            User that triggered the event.

        old_description, new_description (``str``, *optional*):
            Previous and new chat description.
            For :obj:`~pyrogram.enums.ChatEventAction.DESCRIPTION_CHANGED` action only.

        old_history_ttl, new_history_ttl (``int``, *optional*):
            Previous and new chat history TTL.
            For :obj:`~pyrogram.enums.ChatEventAction.HISTORY_TTL_CHANGED` action only.

        old_linked_chat, new_linked_chat (:obj:`~pyrogram.types.Chat`, *optional*):
            Previous and new linked chat.
            For :obj:`~pyrogram.enums.ChatEventAction.LINKED_CHAT_CHANGED` action only.

        old_photo, new_photo (:obj:`~pyrogram.types.Photo`, *optional*):
            Previous and new chat photo.
            For :obj:`~pyrogram.enums.ChatEventAction.PHOTO_CHANGED` action only.

        old_title, new_title (``str``, *optional*):
            Previous and new chat title.
            For :obj:`~pyrogram.enums.ChatEventAction.TITLE_CHANGED` action only.

        old_username, new_username (``str``, *optional*):
            Previous and new chat username.
            For :obj:`~pyrogram.enums.ChatEventAction.USERNAME_CHANGED` action only.

        old_chat_permissions, new_chat_permissions (:obj:`~pyrogram.types.ChatPermissions`, *optional*):
            Previous and new default chat permissions.
            For :obj:`~pyrogram.enums.ChatEventAction.CHAT_PERMISSIONS_CHANGED` action only.

        deleted_message (:obj:`~pyrogram.types.Message`, *optional*):
            Deleted message.
            For :obj:`~pyrogram.enums.ChatEventAction.MESSAGE_DELETED` action only.

        old_message, new_message (:obj:`~pyrogram.types.Message`, *optional*):
            Previous and new message before it has been edited.
            For :obj:`~pyrogram.enums.ChatEventAction.MESSAGE_EDITED` action only.

        invited_member (:obj:`~pyrogram.types.ChatMember`, *optional*):
            New invited chat member.
            For :obj:`~pyrogram.enums.ChatEventAction.MEMBER_INVITED` action only.

        old_administrator_privileges, new_administrator_privileges (:obj:`~pyrogram.types.ChatMember`, *optional*):
            Previous and new administrator privileges.
            For :obj:`~pyrogram.enums.ChatEventAction.ADMINISTRATOR_PRIVILEGES_CHANGED` action only.

        old_member_permissions, new_member_permissions (:obj:`~pyrogram.types.ChatMember`, *optional*):
            Previous and new member permissions.
            For :obj:`~pyrogram.enums.ChatEventAction.MEMBER_PERMISSIONS_CHANGED` action only.

        stopped_poll (:obj:`~pyrogram.types.Message`, *optional*):
            Message containing the stopped poll.
            For :obj:`~pyrogram.enums.ChatEventAction.POLL_STOPPED` action only.

        invites_enabled (``bool``, *optional*):
            If chat invites were enabled (True) or disabled (False).
            For :obj:`~pyrogram.enums.ChatEventAction.INVITES_ENABLED` action only.

        history_hidden (``bool``, *optional*):
            If chat history has been hidden (True) or unhidden (False).
            For :obj:`~pyrogram.enums.ChatEventAction.HISTORY_HIDDEN` action only.

        signatures_enabled (``bool``, *optional*):
            If message signatures were enabled (True) or disabled (False).
            For :obj:`~pyrogram.enums.ChatEventAction.SIGNATURES_ENABLED` action only.

        old_slow_mode, new_slow_mode (``int``, *optional*):
            Previous and new slow mode value in seconds.
            For :obj:`~pyrogram.enums.ChatEventAction.SLOW_MODE_CHANGED` action only.

        pinned_message (:obj:`~pyrogram.types.Message`, *optional*):
            Pinned message.
            For :obj:`~pyrogram.enums.ChatEventAction.MESSAGE_PINNED` action only.

        unpinned_message (:obj:`~pyrogram.types.Message`, *optional*):
            Unpinned message.
            For :obj:`~pyrogram.enums.ChatEventAction.MESSAGE_UNPINNED` action only.

        old_invite_link, new_invite_link (:obj:`~pyrogram.types.ChatInviteLink`, *optional*):
            Previous and new edited invite link.
            For :obj:`~pyrogram.enums.ChatEventAction.INVITE_LINK_EDITED` action only.

        revoked_invite_link (:obj:`~pyrogram.types.ChatInviteLink`, *optional*):
            Revoked invite link.
            For :obj:`~pyrogram.enums.ChatEventAction.INVITE_LINK_REVOKED` action only.

        deleted_invite_link (:obj:`~pyrogram.types.ChatInviteLink`, *optional*):
            Deleted invite link.
            For :obj:`~pyrogram.enums.ChatEventAction.INVITE_LINK_DELETED` action only.
    """

    def __init__(
        self, *,
        id: int,
        date: datetime,
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

        old_administrator_privileges: "types.ChatMember" = None,
        new_administrator_privileges: "types.ChatMember" = None,

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
        deleted_invite_link: "types.ChatInviteLink" = None
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

        self.old_administrator_privileges = old_administrator_privileges
        self.new_administrator_privileges = new_administrator_privileges

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

        old_administrator_privileges: Optional[types.ChatMember] = None
        new_administrator_privileges: Optional[types.ChatMember] = None

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
            action = enums.ChatEventAction.DESCRIPTION_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangeHistoryTTL):
            old_history_ttl = action.prev_value
            new_history_ttl = action.new_value
            action = enums.ChatEventAction.HISTORY_TTL_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangeLinkedChat):
            old_linked_chat = types.Chat._parse_chat(client, chats[action.prev_value])
            new_linked_chat = types.Chat._parse_chat(client, chats[action.new_value])
            action = enums.ChatEventAction.LINKED_CHAT_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangePhoto):
            old_photo = types.Photo._parse(client, action.prev_photo)
            new_photo = types.Photo._parse(client, action.new_photo)
            action = enums.ChatEventAction.PHOTO_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangeTitle):
            old_title = action.prev_value
            new_title = action.new_value
            action = enums.ChatEventAction.TITLE_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionChangeUsername):
            old_username = action.prev_value
            new_username = action.new_value
            action = enums.ChatEventAction.USERNAME_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionDefaultBannedRights):
            old_chat_permissions = types.ChatPermissions._parse(action.prev_banned_rights)
            new_chat_permissions = types.ChatPermissions._parse(action.new_banned_rights)
            action = enums.ChatEventAction.CHAT_PERMISSIONS_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionDeleteMessage):
            deleted_message = await types.Message._parse(client, action.message, users, chats)
            action = enums.ChatEventAction.MESSAGE_DELETED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionEditMessage):
            old_message = await types.Message._parse(client, action.prev_message, users, chats)
            new_message = await types.Message._parse(client, action.new_message, users, chats)
            action = enums.ChatEventAction.MESSAGE_EDITED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantInvite):
            invited_member = types.ChatMember._parse(client, action.participant, users, chats)
            action = enums.ChatEventAction.MEMBER_INVITED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantToggleAdmin):
            old_administrator_privileges = types.ChatMember._parse(client, action.prev_participant, users, chats)
            new_administrator_privileges = types.ChatMember._parse(client, action.new_participant, users, chats)
            action = enums.ChatEventAction.ADMINISTRATOR_PRIVILEGES_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantToggleBan):
            old_member_permissions = types.ChatMember._parse(client, action.prev_participant, users, chats)
            new_member_permissions = types.ChatMember._parse(client, action.new_participant, users, chats)
            action = enums.ChatEventAction.MEMBER_PERMISSIONS_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionStopPoll):
            stopped_poll = await types.Message._parse(client, action.message, users, chats)
            action = enums.ChatEventAction.POLL_STOPPED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantJoin):
            action = enums.ChatEventAction.MEMBER_JOINED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionParticipantLeave):
            action = enums.ChatEventAction.MEMBER_LEFT

        elif isinstance(action, raw.types.ChannelAdminLogEventActionToggleInvites):
            invites_enabled = action.new_value
            action = enums.ChatEventAction.INVITES_ENABLED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionTogglePreHistoryHidden):
            history_hidden = action.new_value
            action = enums.ChatEventAction.HISTORY_HIDDEN

        elif isinstance(action, raw.types.ChannelAdminLogEventActionToggleSignatures):
            signatures_enabled = action.new_value
            action = enums.ChatEventAction.SIGNATURES_ENABLED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionToggleSlowMode):
            old_slow_mode = action.prev_value
            new_slow_mode = action.new_value
            action = enums.ChatEventAction.SLOW_MODE_CHANGED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionUpdatePinned):
            message = action.message

            if message.pinned:
                pinned_message = await types.Message._parse(client, message, users, chats)
                action = enums.ChatEventAction.MESSAGE_PINNED
            else:
                unpinned_message = await types.Message._parse(client, message, users, chats)
                action = enums.ChatEventAction.MESSAGE_UNPINNED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionExportedInviteEdit):
            old_invite_link = types.ChatInviteLink._parse(client, action.prev_invite, users)
            new_invite_link = types.ChatInviteLink._parse(client, action.new_invite, users)
            action = enums.ChatEventAction.INVITE_LINK_EDITED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionExportedInviteRevoke):
            revoked_invite_link = types.ChatInviteLink._parse(client, action.invite, users)
            action = enums.ChatEventAction.INVITE_LINK_REVOKED

        elif isinstance(action, raw.types.ChannelAdminLogEventActionExportedInviteDelete):
            deleted_invite_link = types.ChatInviteLink._parse(client, action.invite, users)
            action = enums.ChatEventAction.INVITE_LINK_DELETED

        else:
            action = f"{enums.ChatEventAction.UNKNOWN}-{action.QUALNAME}"

        return ChatEvent(
            id=event.id,
            date=utils.timestamp_to_datetime(event.date),
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

            old_administrator_privileges=old_administrator_privileges,
            new_administrator_privileges=new_administrator_privileges,

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

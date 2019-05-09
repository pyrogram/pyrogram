# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2019 Dan Tès <https://github.com/delivrance>
#
# This file is part of Pyrogram.
#
# Pyrogram is free software: you can redistribute it and/or modify
# it under the terms of the GNU Lesser General Public License as published
# by the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# Pyrogram is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU Lesser General Public License for more details.
#
# You should have received a copy of the GNU Lesser General Public License
# along with Pyrogram.  If not, see <http://www.gnu.org/licenses/>.

from typing import Union

from pyrogram.api import types
from ..pyrogram_type import PyrogramType


class ChatPermissions(PyrogramType):
    """This object represents both a chat default permissions and a single member permissions within a chat.

    Some permissions make sense depending on the context: default chat permissions, restricted/kicked member or
    administrators in groups or channels.

    Parameters:
        until_date (``int``, *optional*):
            Applicable to restricted and kicked members only.
            Date when user restrictions will be lifted, unix time.
            0 means the restrictions will never be lifted (user restricted forever).

        can_be_edited (``bool``, *optional*):
            Applicable to administrators only.
            True, if you are allowed to edit administrator privileges of the user.

        can_change_info (``bool``, *optional*):
            Applicable to default chat permissions in private groups and administrators in public groups only.
            True, if the chat title, photo and other settings can be changed.

        can_post_messages (``bool``, *optional*):
            Applicable to channel administrators only.
            True, if the administrator can post messages in the channel, channels only.

        can_edit_messages (``bool``, *optional*):
            Applicable to channel administrators only.
            True, if the administrator can edit messages of other users and can pin messages, channels only.

        can_delete_messages (``bool``, *optional*):
            Applicable to administrators only.
            True, if the administrator can delete messages of other users.

        can_restrict_members (``bool``, *optional*):
            Applicable to administrators only.
            True, if the administrator can restrict, ban or unban chat members.

        can_invite_users (``bool``, *optional*):
            Applicable to default chat permissions and administrators only.
            True, if new users can be invited to the chat.

        can_pin_messages (``bool``, *optional*):
            Applicable to default chat permissions in private groups and administrators in public groups only.
            True, if messages can be pinned, supergroups only.

        can_promote_members (``bool``, *optional*):
            Applicable to administrators only.
            True, if the administrator can add new administrators with a subset of his own privileges or demote
            administrators that he has promoted, directly or indirectly (promoted by administrators that were appointed
            by the user).

        can_send_messages (``bool``, *optional*):
            Applicable to default chat permissions and restricted members only.
            True, if text messages, contacts, locations and venues can be sent.

        can_send_media_messages (``bool``, *optional*):
            Applicable to default chat permissions and restricted members only.
            True, if audios, documents, photos, videos, video notes and voice notes can be sent, implies
            can_send_messages.

        can_send_other_messages (``bool``, *optional*):
            Applicable to default chat permissions and restricted members only.
            True, if animations, games, stickers and inline bot results can be sent, implies can_send_media_messages.

        can_add_web_page_previews (``bool``, *optional*):
            Applicable to default chat permissions and restricted members only.
            True, if web page previews can be attached to text messages, implies can_send_media_messages.

        can_send_polls (``bool``, *optional*):
            Applicable to default chat permissions and restricted members only.
            True, if polls can be sent, implies can_send_media_messages.
    """

    __slots__ = [
        "until_date", "can_be_edited", "can_change_info", "can_post_messages", "can_edit_messages",
        "can_delete_messages", "can_restrict_members", "can_invite_users", "can_pin_messages", "can_promote_members",
        "can_send_messages", "can_send_media_messages", "can_send_other_messages", "can_add_web_page_previews",
        "can_send_polls"
    ]

    def __init__(
        self,
        *,
        until_date: int = None,

        # Admin permissions
        can_be_edited: bool = None,
        can_change_info: bool = None,
        can_post_messages: bool = None,  # Channels only
        can_edit_messages: bool = None,  # Channels only
        can_delete_messages: bool = None,
        can_restrict_members: bool = None,
        can_invite_users: bool = None,
        can_pin_messages: bool = None,  # Supergroups only
        can_promote_members: bool = None,

        # Restricted user permissions
        can_send_messages: bool = None,  # Text, contacts, locations and venues
        can_send_media_messages: bool = None,  # Audios, documents, photos, videos, video notes and voice notes
        can_send_other_messages: bool = None,  # Animations (GIFs), games, stickers, inline bot results
        can_add_web_page_previews: bool = None,
        can_send_polls: bool = None
    ):
        super().__init__(None)

        self.until_date = until_date
        self.can_be_edited = can_be_edited

        self.can_change_info = can_change_info
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_delete_messages = can_delete_messages
        self.can_restrict_members = can_restrict_members
        self.can_invite_users = can_invite_users
        self.can_pin_messages = can_pin_messages
        self.can_promote_members = can_promote_members

        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews
        self.can_send_polls = can_send_polls

    @staticmethod
    def _parse(
        entity: Union[
            types.ChannelParticipantAdmin,
            types.ChannelParticipantBanned,
            types.ChatBannedRights
        ]
    ) -> "ChatPermissions":
        if isinstance(entity, types.ChannelParticipantAdmin):
            permissions = entity.admin_rights

            return ChatPermissions(
                can_be_edited=entity.can_edit,
                can_change_info=permissions.change_info,
                can_post_messages=permissions.post_messages,
                can_edit_messages=permissions.edit_messages,
                can_delete_messages=permissions.delete_messages,
                can_restrict_members=permissions.ban_users,
                can_invite_users=permissions.invite_users,
                can_pin_messages=permissions.pin_messages,
                can_promote_members=permissions.add_admins
            )

        if isinstance(entity, (types.ChannelParticipantBanned, types.ChatBannedRights)):
            if isinstance(entity, types.ChannelParticipantBanned):
                denied_permissions = entity.banned_rights  # type: types.ChatBannedRights
            else:
                denied_permissions = entity

            return ChatPermissions(
                until_date=0 if denied_permissions.until_date == (1 << 31) - 1 else denied_permissions.until_date,
                can_send_messages=not denied_permissions.send_messages,
                can_send_media_messages=not denied_permissions.send_media,
                can_send_other_messages=(
                    not denied_permissions.send_stickers or not denied_permissions.send_gifs or
                    not denied_permissions.send_games or not denied_permissions.send_inline
                ),
                can_add_web_page_previews=not denied_permissions.embed_links,
                can_send_polls=not denied_permissions.send_polls,
                can_change_info=not denied_permissions.change_info,
                can_invite_users=not denied_permissions.invite_users,
                can_pin_messages=not denied_permissions.pin_messages
            )

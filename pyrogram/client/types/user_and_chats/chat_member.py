# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

from pyrogram.api import types
from ..pyrogram_type import PyrogramType


class ChatMember(PyrogramType):
    """This object contains information about one member of a chat.

    Args:
        user (:obj:`User <pyrogram.User>`):
            Information about the user.

        status (``str``):
            The member's status in the chat. Can be "creator", "administrator", "member", "restricted",
            "left" or "kicked".

        until_date (``int``, *optional*):
            Restricted and kicked only. Date when restrictions will be lifted for this user, unix time.

        can_be_edited (``bool``, *optional*):
            Administrators only. True, if the bot is allowed to edit administrator privileges of that user.

        can_change_info (``bool``, *optional*):
            Administrators only. True, if the administrator can change the chat title, photo and other settings.

        can_post_messages (``bool``, *optional*):
            Administrators only. True, if the administrator can post in the channel, channels only.

        can_edit_messages (``bool``, *optional*):
            Administrators only. True, if the administrator can edit messages of other users and can pin messages,
            channels only.

        can_delete_messages (``bool``, *optional*):
            Administrators only. True, if the administrator can delete messages of other users.

        can_invite_users (``bool``, *optional*):
            Administrators only. True, if the administrator can invite new users to the chat.

        can_restrict_members (``bool``, *optional*):
            Administrators only. True, if the administrator can restrict, ban or unban chat members.

        can_pin_messages (``bool``, *optional*):
            Administrators only. True, if the administrator can pin messages, supergroups only.

        can_promote_members (``bool``, *optional*):
            Administrators only. True, if the administrator can add new administrators with a subset of his
            own privileges or demote administrators that he has promoted, directly or indirectly (promoted by
            administrators that were appointed by the user).

        can_send_messages (``bool``, *optional*):
            Restricted only. True, if the user can send text messages, contacts, locations and venues.

        can_send_media_messages (``bool``, *optional*):
            Restricted only. True, if the user can send audios, documents, photos, videos, video notes and voice notes,
            implies can_send_messages.

        can_send_other_messages (``bool``, *optional*):
            Restricted only. True, if the user can send animations, games, stickers and use inline bots, implies
            can_send_media_messages.

        can_add_web_page_previews (``bool``, *optional*):
            Restricted only. True, if user may add web page previews to his messages, implies can_send_media_messages.
    """

    def __init__(self,
                 *,
                 client,
                 user,
                 status: str,
                 until_date: int = None,
                 can_be_edited: bool = None,
                 can_change_info: bool = None,
                 can_post_messages: bool = None,
                 can_edit_messages: bool = None,
                 can_delete_messages: bool = None,
                 can_invite_users: bool = None,
                 can_restrict_members: bool = None,
                 can_pin_messages: bool = None,
                 can_promote_members: bool = None,
                 can_send_messages: bool = None,
                 can_send_media_messages: bool = None,
                 can_send_other_messages: bool = None,
                 can_add_web_page_previews: bool = None):
        super().__init__(client)

        self.user = user
        self.status = status
        self.until_date = until_date
        self.can_be_edited = can_be_edited
        self.can_change_info = can_change_info
        self.can_post_messages = can_post_messages
        self.can_edit_messages = can_edit_messages
        self.can_delete_messages = can_delete_messages
        self.can_invite_users = can_invite_users
        self.can_restrict_members = can_restrict_members
        self.can_pin_messages = can_pin_messages
        self.can_promote_members = can_promote_members
        self.can_send_messages = can_send_messages
        self.can_send_media_messages = can_send_media_messages
        self.can_send_other_messages = can_send_other_messages
        self.can_add_web_page_previews = can_add_web_page_previews

    @staticmethod
    def _parse(client, member, user) -> "ChatMember":
        if isinstance(member, (types.ChannelParticipant, types.ChannelParticipantSelf, types.ChatParticipant)):
            return ChatMember(user=user, status="member", client=client)

        if isinstance(member, (types.ChannelParticipantCreator, types.ChatParticipantCreator)):
            return ChatMember(user=user, status="creator", client=client)

        if isinstance(member, types.ChatParticipantAdmin):
            return ChatMember(user=user, status="administrator", client=client)

        if isinstance(member, types.ChannelParticipantAdmin):
            rights = member.admin_rights

            return ChatMember(
                user=user,
                status="administrator",
                can_be_edited=member.can_edit,
                can_change_info=rights.change_info,
                can_post_messages=rights.post_messages,
                can_edit_messages=rights.edit_messages,
                can_delete_messages=rights.delete_messages,
                can_invite_users=rights.invite_users or rights.invite_link,
                can_restrict_members=rights.ban_users,
                can_pin_messages=rights.pin_messages,
                can_promote_members=rights.add_admins,
                client=client
            )

        if isinstance(member, types.ChannelParticipantBanned):
            rights = member.banned_rights

            chat_member = ChatMember(
                user=user,
                status="kicked" if rights.view_messages else "restricted",
                until_date=0 if rights.until_date == (1 << 31) - 1 else rights.until_date,
                client=client
            )

            if chat_member.status == "restricted":
                chat_member.can_send_messages = not rights.send_messages
                chat_member.can_send_media_messages = not rights.send_media
                chat_member.can_send_other_messages = (
                        not rights.send_stickers or not rights.send_gifs or
                        not rights.send_games or not rights.send_inline
                )
                chat_member.can_add_web_page_previews = not rights.embed_links

            return chat_member

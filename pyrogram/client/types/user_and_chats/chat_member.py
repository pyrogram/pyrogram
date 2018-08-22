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

from pyrogram.api.core import Object


class ChatMember(Object):
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

    ID = 0xb0700016

    def __init__(
            self,
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
            can_add_web_page_previews: bool = None
    ):
        self.user = user  # User
        self.status = status  # string
        self.until_date = until_date  # flags.0?int
        self.can_be_edited = can_be_edited  # flags.1?Bool
        self.can_change_info = can_change_info  # flags.2?Bool
        self.can_post_messages = can_post_messages  # flags.3?Bool
        self.can_edit_messages = can_edit_messages  # flags.4?Bool
        self.can_delete_messages = can_delete_messages  # flags.5?Bool
        self.can_invite_users = can_invite_users  # flags.6?Bool
        self.can_restrict_members = can_restrict_members  # flags.7?Bool
        self.can_pin_messages = can_pin_messages  # flags.8?Bool
        self.can_promote_members = can_promote_members  # flags.9?Bool
        self.can_send_messages = can_send_messages  # flags.10?Bool
        self.can_send_media_messages = can_send_media_messages  # flags.11?Bool
        self.can_send_other_messages = can_send_other_messages  # flags.12?Bool
        self.can_add_web_page_previews = can_add_web_page_previews  # flags.13?Bool

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


class Chat(Object):
    """This object represents a chat.

    Args:
        id (``int``):
            Unique identifier for this chat.

        type (``str``):
            Type of chat, can be either "private", "group", "supergroup" or "channel".

        title (``str``, *optional*):
            Title, for supergroups, channels and basic group chats.

        username (``str``, *optional*):
            Username, for private chats, supergroups and channels if available.

        first_name (``str``, *optional*):
            First name of the other party in a private chat.

        last_name (``str``, *optional*):
            Last name of the other party in a private chat.

        all_members_are_administrators (``bool``, *optional*):
            True if a basic group has "All Members Are Admins" enabled.

        photo (:obj:`ChatPhoto <pyrogram.ChatPhoto>`, *optional*):
            Chat photo. Suitable for downloads only.

        description (``str``, *optional*):
            Description, for supergroups and channel chats.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        invite_link (``str``, *optional*):
            Chat invite link, for supergroups and channel chats.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        pinned_message (:obj:`Message <pyrogram.Message>`, *optional*):
            Pinned message, for supergroups and channel chats.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        sticker_set_name (``str``, *optional*):
            For supergroups, name of group sticker set.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        can_set_sticker_set (``bool``, *optional*):
            True, if the group sticker set can be changed by you.
            Returned only in :meth:`get_chat() <pyrogram.Client.get_chat>`.

        members_count (``int``, *optional*):
            Chat members count, for groups and channels only.
    """

    ID = 0xb0700002

    def __init__(
            self,
            id: int,
            type: str,
            title: str = None,
            username: str = None,
            first_name: str = None,
            last_name: str = None,
            all_members_are_administrators: bool = None,
            photo=None,
            description: str = None,
            invite_link: str = None,
            pinned_message=None,
            sticker_set_name: str = None,
            can_set_sticker_set: bool = None,
            members_count: int = None
    ):
        self.id = id
        self.type = type
        self.title = title
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.all_members_are_administrators = all_members_are_administrators
        self.photo = photo
        self.description = description
        self.invite_link = invite_link
        self.pinned_message = pinned_message
        self.sticker_set_name = sticker_set_name
        self.can_set_sticker_set = can_set_sticker_set
        self.members_count = members_count

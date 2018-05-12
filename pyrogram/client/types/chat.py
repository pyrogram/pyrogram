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
            Unique identifier for this chat. This number may be greater than 32 bits and some programming
            languages may have difficulty/silent defects in interpreting it. But it is smaller than 52 bits,
            so a signed 64 bit integer or double-precision float type are safe for storing this identifier.

        type (``str``):
            Type of chat, can be either "private", "group", "supergroup" or "channel".

        title (``str``, *optional*):
            Title, for supergroups, channels and group chats.

        username (``str``, *optional*):
            Username, for private chats, supergroups and channels if available.

        first_name (``str``, *optional*):
            First name of the other party in a private chat.

        last_name (``str``, *optional*):
            Last name of the other party in a private chat.

        all_members_are_administrators (``bool``, *optional*):
            True if a group has 'All Members Are Admins' enabled.

        photo (:obj:`ChatPhoto <pyrogram.ChatPhoto>`, *optional*):
            Chat photo. Returned only in getChat.

        description (``str``, *optional*):
            Description, for supergroups and channel chats. Returned only in getChat.

        invite_link (``str``, *optional*):
            Chat invite link, for supergroups and channel chats. Returned only in getChat.

        pinned_message (:obj:`Message <pyrogram.Message>`, *optional*):
            Pinned message, for supergroups and channel chats. Returned only in getChat.

        sticker_set_name (``str``, *optional*):
            For supergroups, name of group sticker set. Returned only in getChat.

        can_set_sticker_set (``bool``, *optional*):
            True, if the bot can change the group sticker set. Returned only in getChat.
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
            can_set_sticker_set: bool = None
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

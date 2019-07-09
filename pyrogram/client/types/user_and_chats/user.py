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

import pyrogram
from pyrogram.api import types
from .chat_photo import ChatPhoto
from .user_status import UserStatus
from ..pyrogram_type import PyrogramType


class User(PyrogramType):
    """This object represents a Telegram user or bot.

    Args:
        id (``int``):
            Unique identifier for this user or bot.

        is_self(``bool``):
            True, if this user is you yourself.

        is_contact(``bool``):
            True, if this user is in your contacts.

        is_mutual_contact(``bool``):
            True, if you both have each other's contact.

        is_deleted(``bool``):
            True, if this user is deleted.

        is_bot (``bool``):
            True, if this user is a bot.

        first_name (``str``):
            User's or bot's first name.

        status (:obj:`UserStatus <pyrogram.UserStatus>`, *optional*):
            User's Last Seen status. Empty for bots.

        last_name (``str``, *optional*):
            User's or bot's last name.

        username (``str``, *optional*):
            User's or bot's username.

        language_code (``str``, *optional*):
            IETF language tag of the user's language.

        phone_number (``str``, *optional*):
            User's phone number.

        photo (:obj:`ChatPhoto <pyrogram.ChatPhoto>`, *optional*):
            User's or bot's current profile photo. Suitable for downloads only.

        restriction_reason (``str``, *optional*):
            The reason why this bot might be unavailable to some users.
    """

    def __init__(self,
                 *,
                 client: "pyrogram.client.ext.BaseClient",
                 id: int,
                 is_self: bool,
                 is_contact: bool,
                 is_mutual_contact: bool,
                 is_deleted: bool,
                 is_bot: bool,
                 first_name: str,
                 last_name: str = None,
                 status: UserStatus = None,
                 username: str = None,
                 language_code: str = None,
                 phone_number: str = None,
                 photo: ChatPhoto = None,
                 restriction_reason: str = None):
        super().__init__(client)

        self.id = id
        self.is_self = is_self
        self.is_contact = is_contact
        self.is_mutual_contact = is_mutual_contact
        self.is_deleted = is_deleted
        self.is_bot = is_bot
        self.first_name = first_name
        self.last_name = last_name
        self.status = status
        self.username = username
        self.language_code = language_code
        self.phone_number = phone_number
        self.photo = photo
        self.restriction_reason = restriction_reason

    @staticmethod
    def _parse(client, user: types.User) -> "User" or None:
        if user is None:
            return None

        return User(
            id=user.id,
            is_self=user.is_self,
            is_contact=user.contact,
            is_mutual_contact=user.mutual_contact,
            is_deleted=user.deleted,
            is_bot=user.bot,
            first_name=user.first_name,
            last_name=user.last_name,
            status=UserStatus._parse(client, user.status, user.id, user.bot),
            username=user.username,
            language_code=user.lang_code,
            phone_number=user.phone,
            photo=ChatPhoto._parse(client, user.photo),
            restriction_reason=user.restriction_reason,
            client=client
        )
    
    
    
    def block(self):
        """Bound method *block* of :obj:`User`.
        Use as a shortcut for:
        .. code-block:: python
            client.block_user(123456789)
        Example:
            .. code-block:: python
                user.block()
        Returns:
            True on success.
        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.block_user(self.id)


    def unblock(self):
        """Bound method *unblock* of :obj:`User`.
        Use as a shortcut for:
        .. code-block:: python
            client.unblock_user(123456789)
        Example:
            .. code-block:: python
                user.unblock()
        Returns:
            True on success.
        Raises:
            RPCError: In case of a Telegram RPC error.
        """

        return self._client.unblock_user(self.id)
    

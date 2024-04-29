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

from pyrogram import types

from ..object import Object


class RequestChatInfo(Object):
    """Contains information about a chat peer type.

    Parameters:
        button_id (``int``):
            Identifier of button.

        is_creator (``bool``, *optional*):
            If True, returns the list of chats owned by the user.

        is_bot_participant (``bool``, *optional*):
            If True, returns the list of chats with the bot as a member.

        has_username (``bool``, *optional*):
            If True, returns the list of chats with a username.
            If False, returns the list of chats without a username.
            If not specified, no additional restrictions are applied.
            Defaults to None.

        has_forum (``bool``, *optional*):
            If True, returns the list of chats with a forum topics enabled.
            If False, returns the list of chats without a forum topics.
            If not specified, no additional restrictions are applied.
            Defaults to None.

        user_privileges (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
            Privileged actions that an user administrator is able to take.

        bot_privileges (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
            Privileged actions that an bot administrator is able to take.
    """

    def __init__(
        self, *,
        button_id: int,
        is_creator: bool = None,
        is_bot_participant: bool = None,
        has_username: bool = None,
        has_forum: bool = None,
        user_privileges: "types.ChatPrivileges" = None,
        bot_privileges: "types.ChatPrivileges" = None
    ):
        super().__init__()

        self.button_id = button_id
        self.is_creator = is_creator
        self.is_bot_participant = is_bot_participant
        self.has_username = has_username
        self.has_forum = has_forum
        self.user_privileges = user_privileges
        self.bot_privileges = bot_privileges

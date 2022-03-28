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

from pyrogram import raw

from ..object import Object


class BotCommand(Object):
    """A bot command with the standard slash "/" prefix.

    Parameters:
        command (``str``):
            The bot command, for example: "/start".

        description (``str``):
            Description of the bot command.
    """

    def __init__(self, command: str, description: str):
        super().__init__()

        self.command = command
        self.description = description

    def write(self):
        return raw.types.BotCommand(
            command=self.command,
            description=self.description,
        )


class BotCommandScope(Object):
    """
    Represents a scope where the bot commands, specified
    using bots.setBotCommands will be valid.

    Parameters:
        scope (``str``):

            - DEFAULT: The commands will be valid in all chats (default value)

            - PRIVATE: The specified bot commands will only be valid in all private
            chats with users.

            - GROUP: The specified bot commands will be valid in all groups and supergroups

            - GROUP_ADMINS: The specified bot commands will be valid only for chat
            administrators, in all groups and supergroups.

            - PEER: The specified bot commands will be valid only in a specific dialog

            - PEER_ADMINS: The specified bot commands will be valid for all admins of the
            specified group or supergroup.

            - PEER_USER: The specified bot commands will be valid only for a specific user
            in the specified chat
    """

    DEFAULT = "default"
    PRIVATE = "users"
    GROUP = "chats"
    GROUP_ADMINS = "chat_admins"
    PEER = "peer"
    PEER_ADMINS = "peer_admins"
    PEER_USER = "peer_user"

    raw_scopes = {
        DEFAULT: raw.types.BotCommandScopeDefault,
        PRIVATE: raw.types.BotCommandScopeUsers,
        GROUP: raw.types.BotCommandScopeChats,
        GROUP_ADMINS: raw.types.BotCommandScopeChatAdmins,
        PEER: lambda peer: raw.types.BotCommandScopePeer(peer),
        PEER_ADMINS: lambda peer: raw.types.BotCommandScopePeerAdmins(peer),
        PEER_USER: lambda peer, user_id: raw.types.BotCommandScopePeerUser(
            peer, user_id
        ),
    }

    def __init__(
        self,
        scope: str,
        peer: raw.types.InputPeerUser = None,
        user_id: raw.types.InputUser = None,
    ):
        super().__init__()
        self.scope = scope
        self.peer = peer
        self.user_id = user_id

    def write(self):

        if self.scope in ["peer", "peer_admins"]:
            return self.raw_scopes[self.scope](self.peer)

        elif self.scope == "peer_user":
            return self.raw_scopes[self.scopes](self.peer, self.user_id)

        return self.raw_scopes[self.scope]()

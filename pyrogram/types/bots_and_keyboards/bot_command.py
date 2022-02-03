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
            Scope of the command.
    """

    raw_scopes = {
        "default": raw.types.BotCommandScopeDefault(),
        "users": raw.types.BotCommandScopeUsers(),
        "chats": raw.types.BotCommandScopeChats(),
        "chat_admins": raw.types.BotCommandScopeChatAdmins(),
        "peer": lambda peer: raw.types.BotCommandScopePeer(peer),
        "peer_admins": lambda peer: raw.types.BotCommandScopePeerAdmins(peer),
        "peer_user": lambda peer, user_id: raw.types.BotCommandScopePeerUser(
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

        return self.raw_scopes[self.scope]

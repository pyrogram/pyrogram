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
from pyrogram.api import functions, types
from ...ext import BaseClient


class JoinChat(BaseClient):
    async def join_chat(
        self,
        chat_id: str
    ):
        """Use this method to join a group chat or channel.

        Args:
            chat_id (``str``):
                Unique identifier for the target chat in form of a *t.me/joinchat/* link or username of the target
                channel/supergroup (in the format @username).

        Returns:
            On success, a :obj:`Chat <pyrogram.Chat>` object is returned.

        Raises:
            :class:`RPCError <pyrogram.RPCError>` in case of a Telegram RPC error.
        """
        match = self.INVITE_LINK_RE.match(chat_id)

        if match:
            chat = await self.send(
                functions.messages.ImportChatInvite(
                    hash=match.group(1)
                )
            )
            if isinstance(chat.chats[0], types.Chat):
                return pyrogram.Chat._parse_chat_chat(self, chat.chats[0])
            elif isinstance(chat.chats[0], types.Channel):
                return pyrogram.Chat._parse_channel_chat(self, chat.chats[0])
        else:
            resolved_peer = await self.send(
                functions.contacts.ResolveUsername(
                    username=chat_id.lower().strip("@")
                )
            )

            channel = types.InputPeerChannel(
                channel_id=resolved_peer.chats[0].id,
                access_hash=resolved_peer.chats[0].access_hash
            )

            chat = await self.send(
                functions.channels.JoinChannel(
                    channel=channel
                )
            )

            return pyrogram.Chat._parse_channel_chat(self, chat.chats[0])

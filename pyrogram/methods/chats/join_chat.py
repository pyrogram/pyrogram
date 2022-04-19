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

from typing import Union

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold


class JoinChat(Scaffold):
    async def join_chat(
        self,
        chat_id: Union[int, str]
    ) -> "types.Chat":
        """Join a group chat or channel.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat in form of a *t.me/joinchat/* link, a username of the target
                channel/supergroup (in the format @username) or a chat id of a linked chat (channel or supergroup).

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                # Join chat via username
                app.join_chat("pyrogram")

                # Join chat via invite link
                app.join_chat("https://t.me/joinchat/AAAAAE0QmSW3IUmm3UFR7A")

                # Join a linked chat
                app.join_chat(app.get_chat("pyrogram").linked_chat.id)
        """
        match = self.INVITE_LINK_RE.match(str(chat_id))

        if match:
            chat = await self.send(
                raw.functions.messages.ImportChatInvite(
                    hash=match.group(1)
                )
            )
            if isinstance(chat.chats[0], raw.types.Chat):
                return types.Chat._parse_chat_chat(self, chat.chats[0])
            elif isinstance(chat.chats[0], raw.types.Channel):
                return types.Chat._parse_channel_chat(self, chat.chats[0])
        else:
            chat = await self.send(
                raw.functions.channels.JoinChannel(
                    channel=await self.resolve_peer(chat_id)
                )
            )

            return types.Chat._parse_channel_chat(self, chat.chats[0])

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

from pyrogram.api import functions, types, errors
from ...ext import BaseClient, utils


class GetChatMember(BaseClient):
    async def get_chat_member(self,
                        chat_id: int or str,
                        user_id: int or str):
        """Use this method to get information about one member of a chat.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``)::
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            On success, a :obj:`ChatMember <pyrogram.ChatMember>` object is returned.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        chat_id = await self.resolve_peer(chat_id)
        user_id = await self.resolve_peer(user_id)

        if isinstance(chat_id, types.InputPeerChat):
            full_chat = await self.send(
                functions.messages.GetFullChat(
                    chat_id=chat_id.chat_id
                )
            )

            for member in utils.parse_chat_members(full_chat).chat_members:
                if member.user.id == user_id.user_id:
                    return member
            else:
                raise errors.UserNotParticipant
        elif isinstance(chat_id, types.InputPeerChannel):
            r = await self.send(
                functions.channels.GetParticipant(
                    channel=chat_id,
                    user_id=user_id
                )
            )

            return utils.parse_chat_members(
                types.channels.ChannelParticipants(
                    count=1,
                    participants=[r.participant],
                    users=r.users
                )
            ).chat_members[0]
        else:
            raise ValueError("The chat_id \"{}\" belongs to a user".format(chat_id))

#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2021 Dan <https://github.com/delivrance>
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
from pyrogram.scaffold import Scaffold


class DeleteRevokedExportedChatInvites(Scaffold):
    async def delete_revoked_exported_chat_invites(
        self,
        chat_id: Union[int, str],
        admin_id: Union[int, str],
    ) -> bool:
        """Delete already revoked invite links of a specified administrator.
        Owners can clear any administrators revoked links, administrators only their own.

        Parameters:
            chat_id (``int``, ``str``):
                Unique identifier (int) or username (str) of the target chat.

            admin_id (``int`` ``str``):
                Unique identifier (int) or username (str) of the target admin.

        Raises:
            ValueError: In case the chat_id belongs to a user or the admin_id belongs to a chat or channel.

        Returns:
            ``bool``: On success ``True`` is returned.
        """
        peer = await self.resolve_peer(chat_id)
        admin_peer = await self.resolve_peer(admin_id)

        if not isinstance(peer, (raw.types.InputPeerChat, raw.types.InputPeerChannel)):
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user.')

        if not isinstance(admin_peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError(f'The admin_id "{admin_id}" belongs to a chat or channel.')

        return await self.send(
            raw.functions.messages.DeleteRevokedExportedChatInvites(
                peer=peer,
                admin_id=admin_peer,
            )
        )

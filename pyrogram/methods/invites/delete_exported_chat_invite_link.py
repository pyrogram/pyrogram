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


class DeleteExportedChatInviteLink(Scaffold):
    async def delete_exported_chat_invite_link(
        self,
        chat_id: Union[int, str],
        link: str,
    ) -> bool:
        """Delete an invite link that has previously been revoked.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            link (``str``):
                The Invite link or its hash that is to be deleted.

        Raises:
            ValueError:
                In case the chat_id belongs to a user, or the invite link isn't valid, a ValueError is raised.

        Returns:
            ``bool``: On success ``True`` is returned.
        """
        peer = await self.resolve_peer(chat_id)

        match = self.INVITE_LINK_RE.match(link)

        if not match:
            raise ValueError(f'"{link}"" is not a valid invite link.')

        if isinstance(peer, (raw.types.InputPeerChannel, raw.types.InputPeerChat)):
            return await self.send(
                raw.functions.messages.DeleteExportedChatInvite(
                    peer=peer,
                    link=match.group("hash"),
                )
            )
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')


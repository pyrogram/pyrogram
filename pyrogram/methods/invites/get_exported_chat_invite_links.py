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

from typing import Union, List

from pyrogram import raw
from pyrogram import types
from pyrogram.scaffold import Scaffold

class GetExportedChatInviteLinks(Scaffold):
    async def get_exported_chat_invite_links(
        self,
        chat_id: Union[int, str],
        admin_id: Union[int, str],
        limit: int = 0,
        revoked: bool = False,
        offset_date: int = None,
        offset_link: str = None,
    ) -> Union["types.InviteLink", List["types.InviteLink"]]:
        """Get exported invite links in a specific chat.

        .. note::

            As an administrator you can only get your own links you have exported.
            As the chat or channel owner you can get everyones links.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or channel.

            admin_id (``int`` | ``str``):
                Unique identifier for the target admin. For yourself you can use "self" or "me".

            limit (``int``, *optional*):
                How many invite links to get. Defaults to 0, all.

            revoked (``bool``, *optional*):
                Whether or not to get revoked links. Defaults to False.

            offset_date (``int``, *optional*):
                The offset date in unix time taken from the first returned link.
                Can be used to iterate over many exported invite links. Defaults to None.

            offset_link (``str``, *optional*):
                The offset link taken from the first returned link.
                Can be used to iterate over many exported invite links. Defaults to None.

        Raises:
            ValueError: In case the chat_id belongs to a user or the admin_id to a chat or channel.

        Returns:
            :obj:`~pyrogram.types.InviteLink` | List of :obj:`~pyrogram.types.InviteLink`: A single invite link, or a list thereof is returned.
        """
        peer = await self.resolve_peer(chat_id)
        admin_peer = await self.resolve_peer(admin_id)

        if not isinstance(peer, (raw.types.InputPeerChannel, raw.types.InputPeerChat)):
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user.')

        elif not isinstance(admin_peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError(f'The admin_id "{admin_id}" does not belong to a user.')

        else:

            r = await self.send(
                raw.functions.messages.GetExportedChatInvites(
                    peer=peer,
                    admin_id=admin_peer,
                    limit=limit,
                    revoked=revoked,
                    offset_date=offset_date,
                    offset_link=offset_link
                )
            )

            invite_links = types.List()

            for i in r.invites:
                invite_links.append(types.InviteLink._parse(i))

            return invite_links if len(invite_links) > 1 else invite_links[0]

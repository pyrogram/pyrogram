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
from pyrogram import types
from pyrogram.scaffold import Scaffold


class GetChatInviteImporters(Scaffold):
    async def get_chat_invite_importers(
        self,
        chat_id: Union[int, str],
        link: str,
        offset_date: int = 0,
        offset_user: Union[int, str] = "me",
        limit: int = 0,
    ):
        """Get a list of users that have used a specific invite link to join a chat.

        Parameters:
            chat_id (``int``, ``str``):
                Unique identifier (int) or username (str) of the target chat.

            link (str):
                The invite link to check. Entire link or just the hash.

            offset_date (``int``, *optional*):
                Pass a date in Unix time as offset to retrieve only imports from after that date. Defaults to 0.

            offset_user (Union[int, str], optional):
                Pass a unique identifier to a user (``int`` as user_id, ``str`` as @username or phone number) to only
                retrieve users after that. Useful if there are many users that joined via a link.
                Defaults to "me" to start at the first entry.

            limit (int, optional):
                How many joins to retrieve. Defaults to 0, no limit.

        Raises:
            ValueError: In case the chat_id belongs to a user, the offset_user belongs to a chat/channel, or the link is not a valid invite link.

        Returns:
            ``list`` (List of :obj:`~pyrogram.types.InviteImporter`): The list of users that have imported the link. This list may be empty, if nobody has used the link yet.
        """
        peer = await self.resolve_peer(chat_id)
        offset_peer = await self.resolve_peer(offset_user)

        if not isinstance(peer, (raw.types.InputPeerChannel, raw.types.InputPeerChat)):
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user.')

        if not isinstance(offset_peer, (raw.types.InputPeerUser, raw.types.InputPeerSelf)):
            raise ValueError(f'The offset_user "{offset_user}" does not belong to a user.')

        match = self.INVITE_LINK_RE.match(link)

        if not match:
            raise ValueError(f'The link "{link}" is not a valid invite link')

        r = await self.send(
            raw.functions.messages.GetChatInviteImporters(
                peer=peer,
                link=match.group("hash"),
                offset_date=offset_date,
                offset_user=offset_peer,
                limit=limit,
            )
        )

        importers = types.InviteImporter._parse(self, r)

        return importers[0] if len(importers) == 1 else importers

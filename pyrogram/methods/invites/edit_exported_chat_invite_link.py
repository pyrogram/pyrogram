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

class EditExportedChatInviteLink(Scaffold):
    async def edit_exported_chat_invite_link(
        self,
        chat_id: Union[int, str],
        link: str,
        revoked: bool = False,
        expire_date: int = None,
        usage_limit: int = None,
    ) -> types.InviteLink:
        """Edit an exported invite link, or revoke it.

        .. note::

            Expired invite links can be extended with an ``expire_date`` in the future,
            but once revoked they cannot be restored again.

            While administrators can only edit their own invite links, the creator can always edit everyone elses links.

        Parameters:
            chat_id (``int`` | ``str``):
                A unique identifier for the target chat.

            link (``str``):
                The link to be edited. Takes the entire link or just the hash itself.

            revoked (``bool``, *optional*):
                Whether or not the link should be revoked. Once revoked, a link cannot be restored.
                Defaults to ``False``.

            expire_date (``int``, *optional*): 
                Unix time of when the link should expire. Defaults to ``None``.

            usage_limit (``int``, *optional*):
                How many people can use this link to join.
                Defaults to ``None`` for no limit.

        Raises:
            ValueError: In case the chat_id belongs to a user.

        Returns:
            ``str``: On success, the edited invite link is returned.
        """
        peer = await self.resolve_peer(chat_id)

        match = self.INVITE_LINK_RE.match(link)

        if not match:
            raise ValueError(f'The link "{link}" is not valid.')

        if isinstance(peer, (raw.types.InputPeerChannel, raw.types.InputPeerChat)):
            r = await self.send(
                raw.functions.messages.EditExportedChatInvite(
                    peer=peer,
                    link=match.group("hash"),
                    revoked=revoked,
                    expire_date=expire_date,
                    usage_limit=usage_limit,
                )
            )
            return types.InviteLink._parse(r)
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user.')

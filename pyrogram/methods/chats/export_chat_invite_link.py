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


class ExportChatInviteLink(Scaffold):
    async def export_chat_invite_link(
        self,
        chat_id: Union[int, str],
        legacy_revoke_permanent: bool = None,
        expire_date: int = 0,
        usage_limit: int = 0,
    ) -> types.InviteLink:
        """Generate a new invite link for a chat.

        You must be an administrator in the chat for this to work and have the appropriate admin rights.

        .. note ::

            ``legacy_revoke_permanent`` is mutually exclusive with both ``expire_date`` and ``usage_limit``.
            While you can use ``expire_date`` and ``usage_limit`` together,
            you cannot combine either with ``legacy_revoke_permanent``.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

            legacy_revoke_permanent (``bool``, *optional*):
                Whether or not to revoke the "Primary link".
                Mutually exclusive to ``expire_date`` and ``usage_limit``.

            expire_date (``int``, *optional*):
                Unix timestamp of when the exported link should expire.

            usage_limit (``int``, *optional*):
                How many users should be able to use this link to join the chat.

        Returns:
            ``str``: On success, the exported invite link is returned.

        Raises:
            ValueError: In case the chat_id belongs to a user.

        Example:
            .. code-block:: python

                # Revoke the previous Primary Link
                link = app.export_chat_invite_link(chat_id, legacy_revoke_permanent=True)
                print(link)

                # Create a link for up to 7 new users
                link = app.export_chat_invite_link(chat_id, usage_limit=7)
        """
        peer = await self.resolve_peer(chat_id)

        if isinstance(peer, (raw.types.InputPeerChat, raw.types.InputPeerChannel)):
            r = await self.send(
                raw.functions.messages.ExportChatInvite(
                    peer=peer,
                    legacy_revoke_permanent=legacy_revoke_permanent,
                    expire_date=expire_date,
                    usage_limit=usage_limit,
                )
            )

            return types.InviteLink._parse(r)
        else:
            raise ValueError(f'The chat_id "{chat_id}" belongs to a user')

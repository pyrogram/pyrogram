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

from typing import Union

from pyrogram.api import functions, types
from ...ext import BaseClient


class SetCustomTitle(BaseClient):
    async def set_custom_title(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        title: str,
    ) -> bool:
        """Set a custom title to administrators or owners of a supergroup.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            title (``str``, *optional*):
                A custom title that will be shown to all members instead of "Owner" or "Admin".
                Pass None or "" (empty string) to remove the custom title.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Set custom titles to owners or administrators of supergroups
                app.set_custom_title(chat_id, user_id, "Custom Title")
        """
        chat_id = await self.resolve_peer(chat_id)
        user_id = await self.resolve_peer(user_id)

        r = (await self.send(
            functions.channels.GetParticipant(
                channel=chat_id,
                user_id=user_id
            )
        )).participant

        if isinstance(r, types.ChannelParticipantCreator):
            admin_rights = types.ChatAdminRights(
                change_info=True,
                post_messages=True,
                edit_messages=True,
                delete_messages=True,
                ban_users=True,
                invite_users=True,
                pin_messages=True,
                add_admins=True,
            )
        elif isinstance(r, types.ChannelParticipantAdmin):
            admin_rights = r.admin_rights
        else:
            raise ValueError("Custom titles can only be applied to owners or administrators of supergroups")

        await self.send(
            functions.channels.EditAdmin(
                channel=chat_id,
                user_id=user_id,
                admin_rights=admin_rights,
                rank=title
            )
        )

        return True

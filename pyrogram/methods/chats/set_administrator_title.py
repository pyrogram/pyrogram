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


class SetAdministratorTitle(Scaffold):
    async def set_administrator_title(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        title: str,
    ) -> bool:
        """Set a custom title (rank) to an administrator of a supergroup.

        If you are an administrator of a supergroup (i.e. not the owner), you can only set the title of other
        administrators who have been promoted by you. If you are the owner, you can change every administrator's title.

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

                app.set_administrator_title(chat_id, user_id, "ฅ^•ﻌ•^ฅ")
        """
        chat_id = await self.resolve_peer(chat_id)
        user_id = await self.resolve_peer(user_id)

        r = (await self.send(
            raw.functions.channels.GetParticipant(
                channel=chat_id,
                participant=user_id
            )
        )).participant

        if isinstance(r, raw.types.ChannelParticipantCreator):
            admin_rights = raw.types.ChatAdminRights(
                change_info=True,
                post_messages=True,
                edit_messages=True,
                delete_messages=True,
                ban_users=True,
                invite_users=True,
                pin_messages=True,
                add_admins=True,
            )
        elif isinstance(r, raw.types.ChannelParticipantAdmin):
            admin_rights = r.admin_rights
        else:
            raise ValueError("Custom titles can only be applied to owners or administrators of supergroups")

        if not admin_rights.change_info:
            admin_rights.change_info = None

        if not admin_rights.post_messages:
            admin_rights.post_messages = None

        if not admin_rights.edit_messages:
            admin_rights.edit_messages = None

        if not admin_rights.delete_messages:
            admin_rights.delete_messages = None

        if not admin_rights.ban_users:
            admin_rights.ban_users = None

        if not admin_rights.invite_users:
            admin_rights.invite_users = None

        if not admin_rights.pin_messages:
            admin_rights.pin_messages = None

        if not admin_rights.add_admins:
            admin_rights.add_admins = None

        await self.send(
            raw.functions.channels.EditAdmin(
                channel=chat_id,
                user_id=user_id,
                admin_rights=admin_rights,
                rank=title
            )
        )

        return True

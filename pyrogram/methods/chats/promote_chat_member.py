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

import pyrogram
from pyrogram import raw, types, errors


class PromoteChatMember:
    async def promote_chat_member(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        user_id: Union[int, str],
        privileges: "types.ChatPrivileges" = None,
    ) -> bool:
        """Promote or demote a user in a supergroup or a channel.

        You must be an administrator in the chat for this to work and must have the appropriate admin rights.
        Pass False for all boolean parameters to demote a user.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            privileges (:obj:`~pyrogram.types.ChatPrivileges`, *optional*):
                New user privileges.

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Promote chat member to admin
                await app.promote_chat_member(chat_id, user_id)
        """
        chat_id = await self.resolve_peer(chat_id)
        user_id = await self.resolve_peer(user_id)

        # See Chat.promote_member for the reason of this (instead of setting types.ChatPrivileges() as default arg).
        if privileges is None:
            privileges = types.ChatPrivileges()

        try:
            raw_chat_member = (await self.invoke(
                raw.functions.channels.GetParticipant(
                    channel=chat_id,
                    participant=user_id
                )
            )).participant
        except errors.RPCError:
            raw_chat_member = None

        rank = None
        if isinstance(raw_chat_member, raw.types.ChannelParticipantAdmin):
            rank = raw_chat_member.rank

        await self.invoke(
            raw.functions.channels.EditAdmin(
                channel=chat_id,
                user_id=user_id,
                admin_rights=raw.types.ChatAdminRights(
                    anonymous=privileges.is_anonymous,
                    change_info=privileges.can_change_info,
                    post_messages=privileges.can_post_messages,
                    edit_messages=privileges.can_edit_messages,
                    delete_messages=privileges.can_delete_messages,
                    ban_users=privileges.can_restrict_members,
                    invite_users=privileges.can_invite_users,
                    pin_messages=privileges.can_pin_messages,
                    add_admins=privileges.can_promote_members,
                    manage_call=privileges.can_manage_video_chats,
                    other=privileges.can_manage_chat
                ),
                rank=rank or ""
            )
        )

        return True

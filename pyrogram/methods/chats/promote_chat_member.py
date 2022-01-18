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

from pyrogram import raw
from pyrogram.scaffold import Scaffold


class PromoteChatMember(Scaffold):
    async def promote_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        is_anonymous: bool = False,
        can_manage_chat: bool = True,
        can_change_info: bool = False,
        can_post_messages: bool = False,
        can_edit_messages: bool = False,
        can_delete_messages: bool = False,
        can_restrict_members: bool = False,
        can_invite_users: bool = False,
        can_pin_messages: bool = False,
        can_promote_members: bool = False,
        can_manage_voice_chats: bool = False
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

            is_anonymous (``bool``, *optional*):
                Pass True, if the administrator's presence in the chat is hidden.

            can_manage_chat (``bool``, *optional*):
                Pass True, if the administrator can access the chat event log, chat statistics, message statistics
                in channels, see channel members, see anonymous administrators in supergroups and ignore slow mode.
                Implied by any other administrator privilege.

            can_change_info (``bool``, *optional*):
                Pass True, if the administrator can change chat title, photo and other settings.

            can_post_messages (``bool``, *optional*):
                Pass True, if the administrator can create channel posts, channels only.

            can_edit_messages (``bool``, *optional*):
                Pass True, if the administrator can edit messages of other users and can pin messages, channels only.

            can_delete_messages (``bool``, *optional*):
                Pass True, if the administrator can delete messages of other users.

            can_restrict_members (``bool``, *optional*):
                Pass True, if the administrator can restrict, ban or unban chat members.

            can_invite_users (``bool``, *optional*):
                Pass True, if the administrator can invite new users to the chat.

            can_pin_messages (``bool``, *optional*):
                Pass True, if the administrator can pin messages, supergroups only.

            can_promote_members (``bool``, *optional*):
                Pass True, if the administrator can add new administrators with a subset of his own privileges or
                demote administrators that he has promoted, directly or indirectly (promoted by administrators that
                were appointed by him).

            can_manage_voice_chats (``bool``, *optional*):
                Pass True, if the administration can manage voice chats (also called group calls).

        Returns:
            ``bool``: True on success.

        Example:
            .. code-block:: python

                # Promote chat member to supergroup admin
                app.promote_chat_member(chat_id, user_id)
        """
        await self.send(
            raw.functions.channels.EditAdmin(
                channel=await self.resolve_peer(chat_id),
                user_id=await self.resolve_peer(user_id),
                admin_rights=raw.types.ChatAdminRights(
                    anonymous=is_anonymous or None,
                    change_info=can_change_info or None,
                    post_messages=can_post_messages or None,
                    edit_messages=can_edit_messages or None,
                    delete_messages=can_delete_messages or None,
                    ban_users=can_restrict_members or None,
                    invite_users=can_invite_users or None,
                    pin_messages=can_pin_messages or None,
                    add_admins=can_promote_members or None,
                    manage_call=can_manage_voice_chats or None,
                    other=can_manage_chat or None
                ),
                rank=""
            )
        )

        return True

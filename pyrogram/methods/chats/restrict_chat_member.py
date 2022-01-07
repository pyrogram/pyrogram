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
from pyrogram import types
from pyrogram.scaffold import Scaffold


class RestrictChatMember(Scaffold):
    async def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        permissions: "types.ChatPermissions",
        until_date: int = 0
    ) -> "types.Chat":
        """Restrict a user in a supergroup.

        You must be an administrator in the supergroup for this to work and must have the appropriate admin rights.
        Pass True for all permissions to lift restrictions from a user.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            permissions (:obj:`~pyrogram.types.ChatPermissions`):
                New user permissions.

            until_date (``int``, *optional*):
                Date when the user will be unbanned, unix time.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to 0 (ban forever).

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from time import time

                from pyrogram.types import ChatPermissions

                # Completely restrict chat member (mute) forever
                app.restrict_chat_member(chat_id, user_id, ChatPermissions())

                # Chat member muted for 24h
                app.restrict_chat_member(chat_id, user_id, ChatPermissions(), int(time() + 86400))

                # Chat member can only send text messages
                app.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=True))
        """
        r = await self.send(
            raw.functions.channels.EditBanned(
                channel=await self.resolve_peer(chat_id),
                participant=await self.resolve_peer(user_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=until_date,
                    send_messages=True if not permissions.can_send_messages else None,
                    send_media=True if not permissions.can_send_media_messages else None,
                    send_stickers=True if not permissions.can_send_other_messages else None,
                    send_gifs=True if not permissions.can_send_other_messages else None,
                    send_games=True if not permissions.can_send_other_messages else None,
                    send_inline=True if not permissions.can_send_other_messages else None,
                    embed_links=True if not permissions.can_add_web_page_previews else None,
                    send_polls=True if not permissions.can_send_polls else None,
                    change_info=True if not permissions.can_change_info else None,
                    invite_users=True if not permissions.can_invite_users else None,
                    pin_messages=True if not permissions.can_pin_messages else None,
                )
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])

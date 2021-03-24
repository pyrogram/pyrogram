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


class SetChatPermissions(Scaffold):
    async def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: "types.ChatPermissions",
    ) -> "types.Chat":
        """Set default chat permissions for all members.

        You must be an administrator in the group or a supergroup for this to work and must have the
        *can_restrict_members* admin rights.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            permissions (:obj:`~pyrogram.types.ChatPermissions`):
                New default chat permissions.

        Returns:
            :obj:`~pyrogram.types.Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from pyrogram.types import ChatPermissions

                # Completely restrict chat
                app.set_chat_permissions(chat_id, ChatPermissions())

                # Chat members can only send text messages, media, stickers and GIFs
                app.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_stickers=True,
                        can_send_animations=True
                    )
                )
        """
        r = await self.send(
            raw.functions.messages.EditChatDefaultBannedRights(
                peer=await self.resolve_peer(chat_id),
                banned_rights=raw.types.ChatBannedRights(
                    until_date=0,
                    send_messages=True if not permissions.can_send_messages else None,
                    send_media=True if not permissions.can_send_media_messages else None,
                    send_stickers=True if not permissions.can_send_stickers else None,
                    send_gifs=True if not permissions.can_send_animations else None,
                    send_games=True if not permissions.can_send_games else None,
                    send_inline=True if not permissions.can_use_inline_bots else None,
                    embed_links=True if not permissions.can_add_web_page_previews else None,
                    send_polls=True if not permissions.can_send_polls else None,
                    change_info=True if not permissions.can_change_info else None,
                    invite_users=True if not permissions.can_invite_users else None,
                    pin_messages=True if not permissions.can_pin_messages else None,
                )
            )
        )

        return types.Chat._parse_chat(self, r.chats[0])

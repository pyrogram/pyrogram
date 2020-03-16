# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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
from ...types.user_and_chats import Chat, ChatPermissions


class SetChatPermissions(BaseClient):
    def set_chat_permissions(
        self,
        chat_id: Union[int, str],
        permissions: ChatPermissions,
    ) -> Chat:
        """Set default chat permissions for all members.

        You must be an administrator in the group or a supergroup for this to work and must have the
        *can_restrict_members* admin rights.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            permissions (:obj:`ChatPermissions`):
                New default chat permissions.

        Returns:
            :obj:`Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from pyrogram import ChatPermissions

                # Completely restrict chat
                app.set_chat_permissions(chat_id, ChatPermissions())

                # Chat members can only send text messages, media, stickers and GIFs
                app.set_chat_permissions(
                    chat_id,
                    ChatPermissions(
                        can_send_messages=True,
                        can_send_media_messages=True,
                        can_send_other_messages=True
                    )
                )
        """
        send_messages = True
        send_media = True
        send_stickers = True
        send_gifs = True
        send_games = True
        send_inline = True
        embed_links = True
        send_polls = True
        change_info = True
        invite_users = True
        pin_messages = True

        if permissions.can_send_messages:
            send_messages = None

        if permissions.can_send_media_messages:
            send_messages = None
            send_media = None

        if permissions.can_send_other_messages:
            send_messages = None
            send_stickers = None
            send_gifs = None
            send_games = None
            send_inline = None

        if permissions.can_add_web_page_previews:
            send_messages = None
            embed_links = None

        if permissions.can_send_polls:
            send_messages = None
            send_polls = None

        if permissions.can_change_info:
            change_info = None

        if permissions.can_invite_users:
            invite_users = None

        if permissions.can_pin_messages:
            pin_messages = None

        r = self.send(
            functions.messages.EditChatDefaultBannedRights(
                peer=self.resolve_peer(chat_id),
                banned_rights=types.ChatBannedRights(
                    until_date=0,
                    send_messages=send_messages,
                    send_media=send_media,
                    send_stickers=send_stickers,
                    send_gifs=send_gifs,
                    send_games=send_games,
                    send_inline=send_inline,
                    embed_links=embed_links,
                    send_polls=send_polls,
                    change_info=change_info,
                    invite_users=invite_users,
                    pin_messages=pin_messages
                )
            )
        )

        return Chat._parse_chat(self, r.chats[0])

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
from ...types.user_and_chats import Chat, ChatPermissions


class RestrictChatMember(BaseClient):
    async def restrict_chat_member(
        self,
        chat_id: Union[int, str],
        user_id: Union[int, str],
        permissions: ChatPermissions,
        until_date: int = 0
    ) -> Chat:
        """Restrict a user in a supergroup.

        You must be an administrator in the supergroup for this to work and must have the appropriate admin rights.
        Pass True for all permissions to lift restrictions from a user.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            permissions (:obj:`ChatPermissions`):
                New user permissions.

            until_date (``int``, *optional*):
                Date when the user will be unbanned, unix time.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to 0 (ban forever).

        Returns:
            :obj:`Chat`: On success, a chat object is returned.

        Example:
            .. code-block:: python

                from time import time

                from pyrogram import ChatPermissions

                # Completely restrict chat member (mute) forever
                app.restrict_chat_member(chat_id, user_id, ChatPermissions())

                # Chat member muted for 24h
                app.restrict_chat_member(chat_id, user_id, ChatPermissions(), int(time.time() + 86400))

                # Chat member can only send text messages
                app.restrict_chat_member(chat_id, user_id, ChatPermissions(can_send_messages=True))
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

        r = await self.send(
            functions.channels.EditBanned(
                channel=await self.resolve_peer(chat_id),
                user_id=await self.resolve_peer(user_id),
                banned_rights=types.ChatBannedRights(
                    until_date=until_date,
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

# Pyrogram - Telegram MTProto API Client Library for Python
# Copyright (C) 2017-2018 Dan Tès <https://github.com/delivrance>
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

from pyrogram.api import functions, types
from ...ext import BaseClient


class RestrictChatMember(BaseClient):
    def restrict_chat_member(self,
                             chat_id: int or str,
                             user_id: int or str,
                             until_date: int = 0,
                             can_send_messages: bool = False,
                             can_send_media_messages: bool = False,
                             can_send_other_messages: bool = False,
                             can_add_web_page_previews: bool = False):
        """Use this method to restrict a user in a supergroup. The bot must be an administrator in the supergroup for
        this to work and must have the appropriate admin rights. Pass True for all boolean parameters to lift
        restrictions from a user.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For a private channel/supergroup you can use its *t.me/joinchat/* link.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

            until_date (``int``, *optional*):
                Date when the user will be unbanned, unix time.
                If user is banned for more than 366 days or less than 30 seconds from the current time they are
                considered to be banned forever. Defaults to 0 (ban forever).

            can_send_messages (``bool``, *optional*):
                Pass True, if the user can send text messages, contacts, locations and venues.

            can_send_media_messages (``bool``, *optional*):
                Pass True, if the user can send audios, documents, photos, videos, video notes and voice notes,
                implies can_send_messages.

            can_send_other_messages (``bool``, *optional*):
                Pass True, if the user can send animations, games, stickers and use inline bots,
                implies can_send_media_messages.

            can_add_web_page_previews (``bool``, *optional*):
                Pass True, if the user may add web page previews to their messages, implies can_send_media_messages

        Returns:
            True on success.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        send_messages = True
        send_media = True
        send_stickers = True
        send_gifs = True
        send_games = True
        send_inline = True
        embed_links = True

        if can_send_messages:
            send_messages = None

        if can_send_media_messages:
            send_messages = None
            send_media = None

        if can_send_other_messages:
            send_media = None
            send_stickers = None
            send_gifs = None
            send_games = None
            send_inline = None

        if can_add_web_page_previews:
            send_media = None
            embed_links = None

        self.send(
            functions.channels.EditBanned(
                channel=self.resolve_peer(chat_id),
                user_id=self.resolve_peer(user_id),
                banned_rights=types.ChannelBannedRights(
                    until_date=until_date,
                    send_messages=send_messages,
                    send_media=send_media,
                    send_stickers=send_stickers,
                    send_gifs=send_gifs,
                    send_games=send_games,
                    send_inline=send_inline,
                    embed_links=embed_links
                )
            )
        )

        return True

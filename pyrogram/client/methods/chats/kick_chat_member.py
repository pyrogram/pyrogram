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


class KickChatMember(BaseClient):
    def kick_chat_member(self,
                         chat_id: int or str,
                         user_id: int or str,
                         until_date: int = 0):
        """Use this method to kick a user from a group, a supergroup or a channel.
        In the case of supergroups and channels, the user will not be able to return to the group on their own using
        invite links, etc., unless unbanned first. You must be an administrator in the chat for this to work and must
        have the appropriate admin rights.

        Note:
            In regular groups (non-supergroups), this method will only work if the "All Members Are Admins" setting is
            off in the target group. Otherwise members may only be removed by the group's creator or by the member
            that added them.

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

        Returns:
            True on success.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        chat_peer = self.resolve_peer(chat_id)
        user_peer = self.resolve_peer(user_id)

        if isinstance(chat_peer, types.InputPeerChannel):
            self.send(
                functions.channels.EditBanned(
                    channel=chat_peer,
                    user_id=user_peer,
                    banned_rights=types.ChannelBannedRights(
                        until_date=until_date,
                        view_messages=True,
                        send_messages=True,
                        send_media=True,
                        send_stickers=True,
                        send_gifs=True,
                        send_games=True,
                        send_inline=True,
                        embed_links=True
                    )
                )
            )
        else:
            self.send(
                functions.messages.DeleteChatUser(
                    chat_id=abs(chat_id),
                    user_id=user_peer
                )
            )

        return True

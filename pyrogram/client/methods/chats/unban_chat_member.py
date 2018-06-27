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


class UnbanChatMember(BaseClient):
    def unban_chat_member(self,
                          chat_id: int or str,
                          user_id: int or str):
        """Use this method to unban a previously kicked user in a supergroup or channel.
        The user will **not** return to the group or channel automatically, but will be able to join via link, etc.
        You must be an administrator for this to work.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For a private channel/supergroup you can use its *t.me/joinchat/* link.

            user_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target user.
                For a contact that exists in your Telegram address book you can use his phone number (str).

        Returns:
            True on success.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        self.send(
            functions.channels.EditBanned(
                channel=self.resolve_peer(chat_id),
                user_id=self.resolve_peer(user_id),
                banned_rights=types.ChannelBannedRights(
                    until_date=0
                )
            )
        )

        return True

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
from pyrogram.api.errors import ChatAdminRequired
from ...ext import BaseClient


class ExportChatInviteLink(BaseClient):
    def export_chat_invite_link(self, chat_id: int or str, new: bool = False):
        """Use this method to export an invite link to a supergroup or a channel.

        The user must be an administrator in the chat for this to work and must have the appropriate admin rights.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier for the target chat or username of the target channel/supergroup
                (in the format @username).

            new (``bool``):
                The previous link will be deactivated and a new link will be generated.
                This is also used to create the invite link in case it doesn't exist yet.

        Returns:
            On success, the exported invite link as string is returned.

        Raises:
            :class:`Error <pyrogram.Error>`

        Note:
            If the returned link is a new one it may take a while for it to be activated.
        """
        peer = self.resolve_peer(chat_id)

        if isinstance(peer, types.InputPeerChat):
            if new:
                return self.send(
                    functions.messages.ExportChatInvite(
                        chat_id=peer.chat_id
                    )
                ).link
            else:
                chat_full = self.send(
                    functions.messages.GetFullChat(
                        chat_id=peer.chat_id
                    )
                ).full_chat  # type: types.ChatFull

                if isinstance(chat_full.exported_invite, types.ChatInviteExported):
                    return chat_full.exported_invite.link
                else:
                    raise ChatAdminRequired
        elif isinstance(peer, types.InputPeerChannel):
            if new:
                return self.send(
                    functions.channels.ExportInvite(
                        channel=peer
                    )
                ).link
            else:
                channel_full = self.send(
                    functions.channels.GetFullChannel(
                        channel=peer
                    )
                ).full_chat  # type: types.ChannelFull

                if isinstance(channel_full.exported_invite, types.ChatInviteExported):
                    return channel_full.exported_invite.link
                else:
                    raise ChatAdminRequired

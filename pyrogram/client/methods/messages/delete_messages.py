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
from pyrogram.client.ext import BaseClient


class DeleteMessages(BaseClient):
    def delete_messages(self,
                        chat_id: int or str,
                        message_ids,
                        revoke: bool = True):
        """Use this method to delete messages, including service messages, with the following limitations:

        - A message can only be deleted if it was sent less than 48 hours ago.
        - Users can delete outgoing messages in groups and supergroups.
        - Users granted *can_post_messages* permissions can delete outgoing messages in channels.
        - If the user is an administrator of a group, it can delete any message there.
        - If the user has *can_delete_messages* permission in a supergroup or a channel, it can delete any message there.

        Args:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).
                For a private channel/supergroup you can use its *t.me/joinchat/* link.

            message_ids (``iterable``):
                A list of Message identifiers to delete or a single message id.
                Iterators and Generators are also accepted.

            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

        Returns:
            True on success.

        Raises:
            :class:`Error <pyrogram.Error>`
        """
        peer = self.resolve_peer(chat_id)
        message_ids = list(message_ids) if not isinstance(message_ids, int) else [message_ids]

        if isinstance(peer, types.InputPeerChannel):
            self.send(
                functions.channels.DeleteMessages(
                    channel=peer,
                    id=message_ids
                )
            )
        else:
            self.send(
                functions.messages.DeleteMessages(
                    id=message_ids,
                    revoke=revoke or None
                )
            )

        return True

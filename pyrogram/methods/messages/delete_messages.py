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

from typing import Union, Iterable

from pyrogram import raw
from pyrogram.scaffold import Scaffold


class DeleteMessages(Scaffold):
    async def delete_messages(
        self,
        chat_id: Union[int, str],
        message_ids: Union[int, Iterable[int]],
        revoke: bool = True
    ) -> bool:
        """Delete messages, including service messages.

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_ids (``int`` | ``Iterable[int]``):
                A list of Message identifiers to delete (integers) or a single message id.
                Iterators and Generators are also accepted.

            revoke (``bool``, *optional*):
                Deletes messages on both parts.
                This is only for private cloud chats and normal groups, messages on
                channels and supergroups are always revoked (i.e.: deleted for everyone).
                Defaults to True.

        Returns:
            ``bool``: True on success, False otherwise.

        Example:
            .. code-block:: python

                # Delete one message
                app.delete_messages(chat_id, message_id)

                # Delete multiple messages at once
                app.delete_messages(chat_id, list_of_message_ids)

                # Delete messages only on your side (without revoking)
                app.delete_messages(chat_id, message_id, revoke=False)
        """
        peer = await self.resolve_peer(chat_id)
        message_ids = list(message_ids) if not isinstance(message_ids, int) else [message_ids]

        if isinstance(peer, raw.types.InputPeerChannel):
            r = await self.send(
                raw.functions.channels.DeleteMessages(
                    channel=peer,
                    id=message_ids
                )
            )
        else:
            r = await self.send(
                raw.functions.messages.DeleteMessages(
                    id=message_ids,
                    revoke=revoke or None
                )
            )

        # Deleting messages you don't have right onto, won't raise any error.
        # Check for pts_count, which is 0 in case deletes fail.
        return bool(r.pts_count)

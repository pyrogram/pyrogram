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

import pyrogram
from pyrogram import raw, types, utils
from ..object import Object


class MessageStory(Object):
    """Contains information about a forwarded story.

    Parameters:
        chat_id (``int``):
            Unique user identifier of story sender.

        story_id (``int``):
            Unique story identifier.

    """

    def __init__(
        self,
        *,
        chat: "types.Chat",
        story_id: int
    ):
        super().__init__()

        self.chat = chat
        self.story_id = story_id

    @staticmethod
    def _parse(client: "pyrogram.Client", message_story: "raw.types.MessageMediaStory", users, chats) -> "MessageStory":
        peer_id = utils.get_raw_peer_id(message_story.peer)

        if isinstance(message_story.peer, raw.types.PeerChannel):
            chat = types.Chat._parse_channel_chat(client, chats.get(peer_id, None))
        else:
            chat = types.Chat._parse_user_chat(client, users.get(peer_id, None))

        return MessageStory(
            chat=chat,
            story_id=message_story.id
        )

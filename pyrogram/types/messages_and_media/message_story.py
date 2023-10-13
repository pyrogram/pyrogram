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

from pyrogram import raw
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
        chat_id: int,
        story_id: int
    ):
        super().__init__()

        self.chat_id = chat_id
        self.story_id = story_id

    @staticmethod
    def _parse(message_story: "raw.types.MessageMediaStory") -> "MessageStory":
        if isinstance(message_story.peer, raw.types.PeerChannel):
            chat_id = message_story.peer.channel_id
        else:
            chat_id = message_story.peer.user_id

        return MessageStory(
            chat_id=chat_id,
            story_id=message_story.id
        )

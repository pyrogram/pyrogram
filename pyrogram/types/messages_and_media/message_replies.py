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
from typing import List, Union

import pyrogram
from pyrogram import raw
from ..object import Object


class MessageReplies(Object):
    """
    Info about the comment section of a channel post, or a simple message thread.

    Parameters:
        replies (int 32-bit) – Contains the total number of replies in this thread or comment section.

        replies_pts (int 32-bit) – PTS of the message that started this thread.

        comments (bool, optional) – Whether this constructor contains information about the comment section of a channel post, or a simple message thread.

        recent_repliers (List of Peer, optional) – For channel post comments, contains information about the last few comment posters for a specific thread, to show a small list of commenter profile pictures in client previews.

        channel_id (int 64-bit, optional) – For channel post comments, contains the ID of the associated discussion supergroup.

        max_id (int 32-bit, optional) – ID of the latest message in this thread or comment section.

        read_max_id (int 32-bit, optional) – Contains the ID of the latest read message in this thread or comment section.


    """

    def __init__(self, *, client: "pyrogram.Client" = None, replies: int, replies_pts: int,
                 comments: bool = None, recent_repliers: List[raw.types.PeerChannel] = None,
                 channel_id: int = None, max_id: int = None, read_max_id: int = None):
        super().__init__(client)

        self.replies = replies
        self.replies_pts = replies_pts
        self.comments = comments
        self.recent_repliers = recent_repliers
        self.channel_id = channel_id
        self.max_id = max_id
        self.read_max_id = read_max_id

    @staticmethod
    def _parse(client, message_replies: "raw.types.MessageReplies") -> "MessageReplies":
        return MessageReplies(
            replies=message_replies.replies,
            replies_pts=message_replies.replies_pts,
            comments=message_replies.comments,
            recent_repliers=message_replies.recent_repliers,
            channel_id=message_replies.channel_id,
            max_id=message_replies.max_id,
            read_max_id=message_replies.read_max_id,
            client=client
        )

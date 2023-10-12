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

from pyrogram import raw, types
from typing import Union
from ..object import Object


class ForumTopic(Object):
    # todo
    # notify_settings: `~pyrogram.types.PeerNotifySettings`
    # draft: `~pyrogram.types.DraftMessage`
    """A forum topic.

    Parameters:
        id (``Integer``):
            Id of the topic

        date (``Integer``):
            Date topic created

        title (``String``):
            Name of the topic

        icon_color (``Integer``):
            Color of the topic icon in RGB format

        top_message (``Integer``):
            N/A

        read_inbox_max_id (``Integer``):
            N/A

        read_outbox_max_id (``Integer``):
            N/A

        unread_count (``Integer``):
            N/A

        unread_mentions_count (``Integer``):
            N/A

        unread_reactions_count (``Integer``):
            N/A

        from_id (:obj:`~pyrogram.types.PeerChannel` | :obj:`~pyrogram.types.PeerUser`):
            Topic creator.

        my (``Boolean``, *optional*):
            N/A

        closed (``Boolean``, *optional*):
            N/A

        pinned (``Boolean``, *optional*):
            N/A

        short (``Boolean``, *optional*):
            N/A

        icon_emoji_id (``Integer``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon
    """

    def __init__(
        self,
        *,
        id: int,
        date: int,
        title: str,
        icon_color: int,
        top_message: int,
        read_inbox_max_id: int,
        read_outbox_max_id: int,
        unread_count: int,
        unread_mentions_count: int,
        unread_reactions_count: int,
        from_id: Union["types.PeerChannel", "types.PeerUser"],
        # notify_settings: "types.PeerNotifySettings", //todo
        my: bool = None,
        closed: bool = None,
        pinned: bool = None,
        short: bool = None,
        icon_emoji_id: int = None,
        # draft: "types.DraftMessage" = None //todo
    ):
        super().__init__()

        self.id = id
        self.date = date
        self.title = title
        self.icon_color = icon_color
        self.top_message = top_message
        self.read_inbox_max_id = read_inbox_max_id
        self.read_outbox_max_id = read_outbox_max_id
        self.unread_count = unread_count
        self.unread_mentions_count = unread_mentions_count
        self.unread_reactions_count = unread_reactions_count
        self.from_id = from_id
        # self.notify_settings = notify_settings //todo
        self.my = my
        self.closed = closed
        self.pinned = pinned
        self.short = short
        self.icon_emoji_id = icon_emoji_id
        # self.draft = draft //todo

    @staticmethod
    def _parse(forum_topic: "raw.types.forum_topic") -> "ForumTopic":
        from_id = forum_topic.from_id
        if isinstance(from_id, raw.types.PeerChannel):
            peer = types.PeerChannel._parse(from_id)
        if isinstance(from_id, raw.types.PeerUser):
            peer = types.PeerUser._parse(from_id)

        return ForumTopic(
            id=getattr(forum_topic, "id", None),
            date=getattr(forum_topic, "date", None),
            title=getattr(forum_topic, "title", None),
            icon_color=getattr(forum_topic, "icon_color", None),
            top_message=getattr(forum_topic, "top_message", None),
            read_inbox_max_id=getattr(forum_topic, "read_inbox_max_id", None),
            read_outbox_max_id=getattr(forum_topic, "read_outbox_max_id", None),
            unread_count=getattr(forum_topic, "unread_count", None),
            unread_mentions_count=getattr(forum_topic, "unread_mentions_count", None),
            unread_reactions_count=getattr(forum_topic, "unread_reactions_count", None),
            from_id=peer,
            # notify_settings=None, //todo
            my=getattr(forum_topic, "my", None),
            closed=getattr(forum_topic, "closed", None),
            pinned=getattr(forum_topic, "pinned", None),
            short=getattr(forum_topic, "short", None),
            icon_emoji_id=getattr(forum_topic, "icon_emoji_id", None),
            # draft=None //todo
        )

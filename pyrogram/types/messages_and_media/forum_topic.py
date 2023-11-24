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

from pyrogram import raw, utils
from ..object import Object


class ForumTopic(Object):
    """A forum topic.

    Parameters:
        id (``int``):
            Unique topic identifier inside this chat.

        date (``int``):
            Date when the topic was created.

        title (``str``):
            The topic title.

        icon_color (``int``):
            Color of the topic icon in RGB format

        icon_emoji_id (``int``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon

        top_message (``int``):
            The last message sent in the topic at this time.

        unread_count (``int``):
            Amount of unread messages in this topic.

        unread_mentions_count (``int``):
            Amount of unread messages containing a mention in this topic.

        unread_reactions_count (``int``):
            Amount of unread messages containing a reaction in this topic.

        is_my (``bool``, *optional*):
            True, if you are creator of topic.

        is_closed (``bool``, *optional*):
            True, if the topic is closed.

        is_pinned (``bool``, *optional*):
            True, if the topic is pinned.
    """

    def __init__(
        self,
        *,
        id: int,
        date: int,
        title: str,
        icon_color: int,
        icon_emoji_id: int = None,
        top_message: int,
        unread_count: int,
        unread_mentions_count: int,
        unread_reactions_count: int,
        is_my: bool = None,
        is_closed: bool = None,
        is_pinned: bool = None,
    ):
        super().__init__()

        self.id = id
        self.date = date
        self.title = title
        self.icon_color = icon_color
        self.icon_emoji_id = icon_emoji_id
        self.top_message = top_message
        self.unread_count = unread_count
        self.unread_mentions_count = unread_mentions_count
        self.unread_reactions_count = unread_reactions_count
        self.is_my = is_my
        self.is_closed = is_closed
        self.is_pinned = is_pinned

    @staticmethod
    def _parse(forum_topic: "raw.types.ForumTopic") -> "ForumTopic":
        return ForumTopic(
            id=forum_topic.id,
            date=utils.timestamp_to_datetime(forum_topic.date),
            title=forum_topic.title,
            icon_color=getattr(forum_topic, "icon_color", None),
            icon_emoji_id=getattr(forum_topic, "icon_emoji_id", None),
            top_message=getattr(forum_topic, "top_message", None),
            unread_count=getattr(forum_topic, "unread_count", None),
            unread_mentions_count=getattr(forum_topic, "unread_mentions_count", None),
            unread_reactions_count=getattr(forum_topic, "unread_reactions_count", None),
            is_my=getattr(forum_topic, "my", None),
            is_closed=getattr(forum_topic, "closed", None),
            is_pinned=getattr(forum_topic, "pinned", None),
        )

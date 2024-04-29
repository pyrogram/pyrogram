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

from datetime import datetime

import pyrogram
from pyrogram import types, raw, utils
from ..object import Object


class ForumTopic(Object):
    """A forum topic.

    Parameters:
        id (``int``):
            Unique topic identifier inside this chat.

        title (``str``):
            The topic title.

        date (:py:obj:`~datetime.datetime`, *optional*):
            Date when the topic was created.

        icon_color (``str``, *optional*):
            Color of the topic icon in HEX format

        icon_emoji_id (``int``, *optional*):
            Unique identifier of the custom emoji shown as the topic icon

        creator (:obj:`~pyrogram.types.Chat`, *optional*):
            Topic creator.

        top_message (:obj:`~pyrogram.types.Message`, *optional*):
            The last message sent in the topic at this time.

        unread_count (``int``, *optional*):
            Amount of unread messages in this topic.

        unread_mentions_count (``int``, *optional*):
            Amount of unread messages containing a mention in this topic.

        unread_reactions_count (``int``, *optional*):
            Amount of unread messages containing a reaction in this topic.

        is_my (``bool``, *optional*):
            True, if you are creator of topic.

        is_closed (``bool``, *optional*):
            True, if the topic is closed.

        is_pinned (``bool``, *optional*):
            True, if the topic is pinned.

        is_short (``bool``, *optional*):
            True, if the topic is short.

        is_hidden (``bool``, *optional*):
            True, if the topic is hidden.

        is_deleted (``bool``, *optional*):
            The forum topic is deleted.
    """

    def __init__(
        self,
        *,
        id: int,
        title: str = None,
        date: datetime = None,
        icon_color: str = None,
        icon_emoji_id: int = None,
        creator: "types.Chat" = None,
        top_message: "types.Message" = None,
        unread_count: int = None,
        unread_mentions_count: int = None,
        unread_reactions_count: int = None,
        is_my: bool = None,
        is_closed: bool = None,
        is_pinned: bool = None,
        is_short: bool = None,
        is_hidden: bool = None,
        is_deleted: bool = None
    ):
        super().__init__()

        self.id = id
        self.title = title
        self.date = date
        self.icon_color = icon_color
        self.icon_emoji_id = icon_emoji_id
        self.creator = creator
        self.top_message = top_message
        self.unread_count = unread_count
        self.unread_mentions_count = unread_mentions_count
        self.unread_reactions_count = unread_reactions_count
        self.is_my = is_my
        self.is_closed = is_closed
        self.is_pinned = is_pinned
        self.is_short = is_short
        self.is_hidden = is_hidden
        self.is_deleted = is_deleted

    @staticmethod
    def _parse(client: "pyrogram.Client", forum_topic: "raw.types.ForumTopic", messages: dict = {},  users: dict = {}, chats: dict = {}) -> "ForumTopic":
        if isinstance(forum_topic, raw.types.ForumTopicDeleted):
            return ForumTopic(id=forum_topic.id, is_deleted=True)

        creator = None

        peer = getattr(forum_topic, "from_id", None)

        if peer:
            peer_id = utils.get_raw_peer_id(peer)

            if isinstance(peer, raw.types.PeerUser):
                creator = types.Chat._parse_user_chat(client, users[peer_id])
            else:
                creator = types.Chat._parse_channel_chat(client, chats[peer_id])

        return ForumTopic(
            id=forum_topic.id,
            title=forum_topic.title,
            date=utils.timestamp_to_datetime(forum_topic.date),
            icon_color=format(forum_topic.icon_color, "x") if getattr(forum_topic, "icon_color", None) else None,
            icon_emoji_id=getattr(forum_topic, "icon_emoji_id", None),
            creator=creator,
            top_message=messages.get(getattr(forum_topic, "top_message", None)),
            unread_count=getattr(forum_topic, "unread_count", None),
            unread_mentions_count=getattr(forum_topic, "unread_mentions_count", None),
            unread_reactions_count=getattr(forum_topic, "unread_reactions_count", None),
            is_my=getattr(forum_topic, "my", None),
            is_closed=getattr(forum_topic, "closed", None),
            is_pinned=getattr(forum_topic, "pinned", None),
            is_short=getattr(forum_topic, "short", None),
            is_hidden=getattr(forum_topic, "hidden", None),
        )

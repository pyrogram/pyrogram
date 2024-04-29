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

from typing import Union, AsyncGenerator

import pyrogram
from pyrogram import types, raw, utils


class GetForumTopics:
    async def get_forum_topics(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0
    ) -> AsyncGenerator["types.ForumTopic", None]:
        """Get one or more topic from a chat.

        .. include:: /_includes/usable-by/users.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.

            limit (``int``, *optional*):
                Limits the number of topics to be retrieved.
                By default, no limit is applied and all topics are returned.

        Returns:
            ``Generator``: A generator yielding :obj:`~pyrogram.types.ForumTopic` objects.

        Example:
            .. code-block:: python

                # Iterate through all topics
                async for topic in app.get_forum_topics(chat_id):
                    print(topic)
        """
        current = 0
        total = limit or (1 << 31) - 1
        limit = min(100, total)

        offset_date = 0
        offset_id = 0
        offset_topic = 0

        while True:
            r = await self.invoke(
                raw.functions.channels.GetForumTopics(
                    channel=await self.resolve_peer(chat_id),
                    offset_date=offset_date,
                    offset_id=offset_id,
                    offset_topic=offset_topic,
                    limit=limit
                )
            )

            users = {i.id: i for i in r.users}
            chats = {i.id: i for i in r.chats}

            messages = {}

            for message in r.messages:
                if isinstance(message, raw.types.MessageEmpty):
                    continue

                messages[message.id] = await types.Message._parse(self, message, users, chats)

            topics = []

            for topic in r.topics:
                topics.append(types.ForumTopic._parse(self, topic, messages, users, chats))

            if not topics:
                return

            last = topics[-1]

            offset_id = last.top_message.id
            offset_date = utils.datetime_to_timestamp(last.top_message.date)
            offset_topic = last.id

            for topic in topics:
                yield topic

                current += 1

                if current >= total:
                    return

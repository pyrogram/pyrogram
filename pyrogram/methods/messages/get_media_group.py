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

import logging
from typing import Union, List

import pyrogram
from pyrogram import types

log = logging.getLogger(__name__)


class GetMediaGroup:
    async def get_media_group(
        self: "pyrogram.Client",
        chat_id: Union[int, str],
        message_id: int
    ) -> List["types.Message"]:
        """Get the media group a message belongs to.

        .. include:: /_includes/usable-by/users-bots.rst

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (``int``):
                The id of one of the messages that belong to the media group.
                
        Returns:
            List of :obj:`~pyrogram.types.Message`: On success, a list of messages of the media group is returned.
            
        Raises:
            ValueError: 
                In case the passed message_id is negative or equal 0. 
                In case target message doesn't belong to a media group.
        """

        if message_id <= 0:
            raise ValueError("Passed message_id is negative or equal to zero.")

        # Get messages with id from `id - 9` to `id + 10` to get all possible media group messages.
        messages = await self.get_messages(
            chat_id=chat_id,
            message_ids=[msg_id for msg_id in range(message_id - 9, message_id + 10)],
            replies=0
        )

        # There can be maximum 10 items in a media group.
        # If/else condition to fix the problem of getting correct `media_group_id` when `message_id` is less than 10.
        media_group_id = messages[9].media_group_id if len(messages) == 19 else messages[message_id - 1].media_group_id

        if media_group_id is None:
            raise ValueError("The message doesn't belong to a media group")

        return types.List(msg for msg in messages if msg.media_group_id == media_group_id)

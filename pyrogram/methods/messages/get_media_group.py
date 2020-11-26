#  Pyrogram - Telegram MTProto API Client Library for Python
#  Copyright (C) 2017-2020 Dan <https://github.com/delivrance>
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

from pyrogram.scaffold import Scaffold
from pyrogram.types import list

log = logging.getLogger(__name__)


class GetMediaGroup(Scaffold):
    async def get_media_group(
        self,
        chat_id: Union[int, str],
        message_id: int
    ) -> List["types.Message"]:
        """Get media group 

        Parameters:
            chat_id (``int`` | ``str``):
                Unique identifier (int) or username (str) of the target chat.
                For your personal cloud (Saved Messages) you can simply use "me" or "self".
                For a contact that exists in your Telegram address book you can use his phone number (str).

            message_id (int):
                #TODO Pass one message of target media get_media_group
        Returns:
            List of :obj:`~pyrogram.types.Message`
        Raises:
            #TODO ValueError: In case message isn't related to media group. 
        """
        messages = await self.get_messages(chat_id, [msg_id for msg_id in range(message_id-9, message_id+10)], replies=0)

        if messages[9].media_group_id:
            media_group_id = messages[9].media_group_id
        else:
            raise ValueError("Message isn't related to media group") #TODO

        return list.List(msg for msg in messages if msg.media_group_id == media_group_id)

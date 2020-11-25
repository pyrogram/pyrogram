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

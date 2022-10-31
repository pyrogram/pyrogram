from datetime import datetime
from typing import Union

import pyrogram
from pyrogram import raw, utils


async def get_chunk_with_replies(
        *,
        client: "pyrogram.Client",
        chat_id: Union[int, str],
        limit: int = 0,
        offset: int = 0,
        from_message_id: int = 0,
        from_date: datetime = utils.zero_datetime()
):
    messages = await client.invoke(
        raw.functions.messages.GetHistory(
            peer=await client.resolve_peer(chat_id),
            offset_id=from_message_id,
            offset_date=utils.datetime_to_timestamp(from_date),
            add_offset=offset,
            limit=limit,
            max_id=0,
            min_id=0,
            hash=0
        ),
        sleep_threshold=60
    )

    return await utils.parse_messages(client, messages)

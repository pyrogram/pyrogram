from typing import Union, List

import pyrogram
from pyrogram import raw
from pyrogram.raw.types import InputNotifyPeer
from pyrogram.raw.types import InputPeerNotifySettings
from pyrogram.raw.functions.account import UpdateNotifySettings
import datetime

class MuteChat:
    async def mute_chat(
        self: "pyrogram.Client",
        chat_ids: Union[int, str],
        second: Union[int]
    ) -> bool:
        """Mute notifications of a chat.
        Returns:
            ``bool``: On success, True is returned.
        Example:
            .. code-block:: python
                await app.mute_chat(chat_id, 3600)
        """

        peer = InputNotifyPeer(peer=await self.resolve_peer(chat_id))
        settings = InputPeerNotifySettings(silent=True, mute_until=int((datetime.datetime.now() + datetime.timedelta(seconds=second)).timestamp()))
        await self.invoke(UpdateNotifySettings(peer=peer, settings=settings))
        return
